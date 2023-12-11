from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from django.views.generic.edit import FormView

from accounts.models import UserBankAccount
from transactions.constants import DEPOSIT, WITHDRAWAL
from transactions.forms import (
    DepositForm,
    TransactionDateRangeForm,
    WithdrawForm, TransferMoneyForm,
)
from transactions.models import Transaction


class TransactionRepostView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    form_data = {}

    def get(self, request, *args, **kwargs):
        form = TransactionDateRangeForm(request.GET or None)
        if form.is_valid():
            self.form_data = form.cleaned_data

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )

        daterange = self.form_data.get("daterange")

        if daterange:
            queryset = queryset.filter(timestamp__date__range=daterange)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account,
            'form': TransactionDateRangeForm(self.request.GET or None)
        })

        return context


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transactions:transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit Money to Your Account'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        if not account.initial_deposit_date:
            now = timezone.now()
            next_interest_month = int(
                12 / account.account_type.interest_calculation_per_year
            )
            account.initial_deposit_date = now
            account.interest_start_date = (
                    now + relativedelta(
                months=+next_interest_month
            )
            )

        account.balance += amount
        account.save(
            update_fields=[
                'initial_deposit_date',
                'balance',
                'interest_start_date'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )

        return super().form_valid(form)


class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money from Your Account'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        self.request.user.account.balance -= form.cleaned_data.get('amount')
        self.request.user.account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn {"{:,.2f}".format(float(amount))}$ from your account'
        )

        return super().form_valid(form)


class TransferMoneyView(FormView):
    form_class = TransferMoneyForm
    template_name = 'transactions/transfer_money.html'
    success_url = reverse_lazy('transactions:transaction_report')

    def form_valid(self, form):
        recipient_username = form.cleaned_data.get('recipient_username')
        amount = form.cleaned_data.get('amount')

        # Get the sender's account
        sender_account = self.request.user.account

        print(sender_account.balance)

        # Check if the sender has sufficient balance
        if sender_account.balance < amount:
            messages.error(self.request, 'Insufficient balance to transfer.')
            return redirect('transfer_money')

        # Find the recipient's account
        try:
            recipient_account = UserBankAccount.objects.get(user__email=recipient_username)
            print(recipient_account)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Recipient account not found.')
            return redirect('transfer_money')

        # Update balances for both sender and recipient
        sender_account.balance -= amount
        recipient_account.balance += amount

        sender_account.save()
        recipient_account.save()

        transaction = Transaction.objects.create(
            account=recipient_account,
            amount=amount,
            balance_after_transaction=sender_account.balance,
            transaction_type=WITHDRAWAL,
        )
        messages.success(self.request, f'${amount} successfully transferred to {recipient_username}.')
        return super().form_valid(form)
