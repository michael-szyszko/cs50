from debt_db import Debts

# maximum time to pay off debt is 600 months or 50 years
MAXIMUM_MONTHS = 600


def debt_sorter_snowball(debt):
    return float(debt.amount)


def debt_sorter_avalanche(debt):
    return -float(debt.rate)


def debt_sorter_name(debt):
    return debt.name.lower()


def debt_sorter_date(debt):
    return date_hash(debt)


def date_hash(debt):
    return debt.year * 100 + debt.month


def date_hash_next_month(debt):
    if debt.month == 12:
        return (debt.year + 1) * 100 + 1
    else:
        return debt.year * 100 + debt.month + 1


def simulate_debt_paying(debts, extra_payment, sorterKey=debt_sorter_snowball):
    debts_by_month = [[]]
    future_debts = []
    debts.sort(key=sorterKey)
    debts.sort(key=debt_sorter_date)
    first_date_hash = date_hash(debts[0])
    for debt in debts:
        if first_date_hash == date_hash(debt):
            debts_by_month[0].append(debt)
        else:
            future_debts.append(debt)
    user_id = float(debts[-1].user_id)

    extra_payment_this_month = extra_payment
    month_count = 0
    while month_count < MAXIMUM_MONTHS:
        simulated_debts = []

        for debt in debts_by_month[month_count]:
            name = debt.name
            amount = float(debt.amount)
            minimum_payment = float(debt.minimum_payment)
            rate = float(debt.rate)
            debt_id = debt.id
            year = debt.year
            month = debt.month + 1

            if month == 13:
                month = 1
                year += 1

            amount = amount + (amount * (rate / 100.0) / 12)
            if amount == 0:
                extra_payment_this_month = extra_payment_this_month + minimum_payment
            elif amount <= minimum_payment:
                extra_payment_this_month = extra_payment_this_month + (
                    minimum_payment - amount
                )
                amount = 0
            else:
                amount = amount - minimum_payment

            debt = Debts(
                id=debt_id,
                user_id=user_id,
                name=name,
                amount=amount,
                rate=rate,
                minimum_payment=minimum_payment,
                month=month,
                year=year,
            )
            simulated_debts.append(debt)

        # apply all extra payments that include any minimum payments from paid off debts
        for debt in simulated_debts:
            if debt.amount > 0 and extra_payment_this_month > 0:
                if debt.amount >= extra_payment_this_month:
                    debt.amount -= extra_payment_this_month
                    extra_payment_this_month = 0
                else:
                    extra_payment_this_month -= debt.amount
                    debt.amount = 0

        while len(future_debts) > 0 and date_hash(
            future_debts[0]
        ) == date_hash_next_month(debts_by_month[month_count][0]):
            simulated_debts.append(future_debts[0])

            # retroactively add the debt zeroed to the previous month to indicate it as an upcoming debt
            for debts in debts_by_month:
                zero_debt = Debts(
                    id=future_debts[0].id,
                    user_id=future_debts[0].user_id,
                    name=future_debts[0].name,
                    amount=0,
                    rate=0,
                    minimum_payment=0,
                    month=debts[0].month,
                    year=debts[0].year,
                )

                debts.append(zero_debt)
            future_debts.pop(0)

        month_count = month_count + 1
        extra_payment_this_month = extra_payment

        # sort debts from smallest to largest
        simulated_debts.sort(key=sorterKey)

        debts_by_month.append(simulated_debts)
        if debts_paid(simulated_debts):
            return debts_by_month
    return debts_by_month


def debts_paid(debts):
    for debt in debts:
        if float(debt.amount) > 0:
            return False
    return True
