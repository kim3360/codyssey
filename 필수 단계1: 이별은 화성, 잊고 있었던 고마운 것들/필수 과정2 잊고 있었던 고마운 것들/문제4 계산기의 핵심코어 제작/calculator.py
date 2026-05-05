from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext

getcontext().prec = 40


class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self._entry = '0'
        self._stored = None
        self._pending_op = None
        self._fresh = True
        self._error = False

    def press_digit(self, digit):
        if self._error:
            return
        if len(digit) != 1 or not digit.isdigit():
            return
        if self._fresh:
            self._entry = digit
            self._fresh = False
        elif self._entry == '0':
            if digit != '0':
                self._entry = digit
        else:
            self._entry += digit

    def press_decimal(self):
        if self._error:
            return
        if self._fresh:
            self._entry = '0.'
            self._fresh = False
            return
        if '.' in self._entry:
            return
        self._entry += '.'

    def negative_positive(self):
        if self._error:
            return
        try:
            value = Decimal(self._entry)
            self._entry = self._decimal_to_string(-value)
        except (InvalidOperation, OverflowError):
            self._set_error()

    def percent(self):
        if self._error:
            return
        try:
            value = Decimal(self._entry)
            self._entry = self._format_result(value / Decimal(100))
            self._fresh = True
        except (InvalidOperation, OverflowError):
            self._set_error()

    def add(self):
        self._select_operator('add')

    def subtract(self):
        self._select_operator('subtract')

    def multiply(self):
        self._select_operator('multiply')

    def divide(self):
        self._select_operator('divide')

    def equal(self):
        if self._error:
            return
        if self._pending_op is None or self._stored is None:
            self._fresh = True
            return
        try:
            left = Decimal(self._stored)
            right = Decimal(self._entry)
            result = self._apply_binary(self._pending_op, left, right)
            self._entry = self._format_result(result)
            self._stored = None
            self._pending_op = None
            self._fresh = True
        except (InvalidOperation, OverflowError, ZeroDivisionError):
            self._set_error()

    def raw_value(self):
        return self._entry

    def display_value(self):
        if self._error:
            return 'Error'
        return self._format_with_commas(self._entry)

    def _select_operator(self, op):
        if self._error:
            return
        try:
            if (
                self._pending_op is not None
                and self._stored is not None
                and not self._fresh
            ):
                left = Decimal(self._stored)
                right = Decimal(self._entry)
                result = self._apply_binary(self._pending_op, left, right)
                self._entry = self._format_result(result)
                self._stored = self._entry
            else:
                self._stored = self._entry
            self._pending_op = op
            self._fresh = True
        except (InvalidOperation, OverflowError, ZeroDivisionError):
            self._set_error()

    @staticmethod
    def _apply_binary(op, left, right):
        if op == 'add':
            return left + right
        if op == 'subtract':
            return left - right
        if op == 'multiply':
            return left * right
        if op == 'divide':
            if right == 0:
                raise ZeroDivisionError
            return left / right
        raise ValueError('unknown operator')

    def _set_error(self):
        self._error = True
        self._entry = 'Error'

    @staticmethod
    def _decimal_to_string(value):
        text = format(value, 'f')
        if '.' in text:
            text = text.rstrip('0').rstrip('.')
        if text in ('', '-'):
            text = '0'
        return text

    def _format_result(self, value):
        try:
            exponent = value.as_tuple().exponent
        except InvalidOperation:
            raise OverflowError
        if exponent < 0 and -exponent > 6:
            value = value.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
        return self._decimal_to_string(value)

    @staticmethod
    def _format_with_commas(raw):
        negative = raw.startswith('-')
        body = raw[1:] if negative else raw
        if '.' in body:
            int_part, frac_part = body.split('.', 1)
        else:
            int_part, frac_part = body, None
        if not int_part:
            int_part = '0'

        idx = 0
        while idx < len(int_part) - 1 and int_part[idx] == '0':
            idx += 1
        int_part = int_part[idx:]

        out = []
        for i, ch in enumerate(reversed(int_part)):
            if i and i % 3 == 0:
                out.append(',')
            out.append(ch)
        int_fmt = ''.join(reversed(out))
        sign = '-' if negative else ''
        if frac_part is not None:
            return f'{sign}{int_fmt}.{frac_part}'
        return f'{sign}{int_fmt}'


if __name__ == '__main__':
    calc = Calculator()
    calc.press_digit('1')
    calc.press_digit('2')
    calc.add()
    calc.press_digit('3')
    calc.equal()
    print(calc.display_value())
