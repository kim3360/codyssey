import operator
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext

getcontext().prec = 40

_BINOPS = {
    'add': operator.add,
    'subtract': operator.sub,
    'multiply': operator.mul,
    'divide': operator.truediv,
}


class Calculator:
    _OP_SYM = {
        'add': '+',
        'subtract': '-',
        'multiply': '×',
        'divide': '÷',
    }

    def __init__(self):
        self.reset()

    def reset(self):
        self._entry = '0'
        self._stored = None
        self._pending_op = None
        self._fresh = True
        self._error = False
        self._last_pretty = None

    def clear_entry(self):
        if self._error:
            self.reset()
            return
        self._last_pretty = None
        self._entry = '0'
        self._fresh = True

    def is_ac_label(self) -> bool:
        if self._error:
            return True
        return (
            self._entry == '0'
            and self._stored is None
            and self._pending_op is None
        )

    def display_value(self) -> str:
        if self._error:
            return 'Error'
        if self._last_pretty is not None:
            return self._last_pretty
        if self._pending_op is not None and self._stored is not None:
            sym = self._OP_SYM[self._pending_op]
            left_fmt = self._format_with_commas(self._stored)
            if self._fresh:
                return f'{left_fmt} {sym}'
            right_fmt = self._format_with_commas(self._entry)
            return f'{left_fmt} {sym} {right_fmt}'
        return self._format_with_commas(self._entry)

    def press_digit(self, digit: str):
        if self._error:
            return
        self._last_pretty = None
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
        self._last_pretty = None
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
        self._last_pretty = None
        try:
            v = Decimal(self._entry)
            self._entry = self._decimal_to_display_string(-v)
        except (InvalidOperation, OverflowError):
            self._set_error()

    def percent(self):
        if self._error:
            return
        self._last_pretty = None
        try:
            v = Decimal(self._entry)
            self._entry = self._format_result_for_output(v / Decimal(100))
            self._fresh = True
        except (InvalidOperation, OverflowError):
            self._set_error()

    def add(self):
        self._select_op('add')

    def subtract(self):
        self._select_op('subtract')

    def multiply(self):
        self._select_op('multiply')

    def divide(self):
        self._select_op('divide')

    def equal(self):
        if self._error:
            return
        if self._pending_op is None or self._stored is None:
            self._fresh = True
            return
        try:
            left_fmt = self._format_with_commas(self._stored)
            right_fmt = self._format_with_commas(self._entry)
            sym = self._OP_SYM[self._pending_op]
            left = Decimal(self._stored)
            right = Decimal(self._entry)
            result = _BINOPS[self._pending_op](left, right)
            out = self._format_result_for_output(result)
            out_fmt = self._format_with_commas(out)
            self._last_pretty = f'{left_fmt} {sym} {right_fmt} = {out_fmt}'
            self._entry = out
            self._stored = None
            self._pending_op = None
            self._fresh = True
        except (InvalidOperation, OverflowError, ZeroDivisionError):
            self._set_error()

    def _select_op(self, op: str):
        if self._error:
            return
        if op not in _BINOPS:
            return
        self._last_pretty = None
        try:
            if self._pending_op is not None and self._stored is not None and not self._fresh:
                left = Decimal(self._stored)
                right = Decimal(self._entry)
                result = _BINOPS[self._pending_op](left, right)
                self._entry = self._format_result_for_output(result)
                self._stored = self._entry
            else:
                self._stored = self._entry
            self._pending_op = op
            self._fresh = True
        except (InvalidOperation, OverflowError, ZeroDivisionError):
            self._set_error()

    def _set_error(self):
        self._error = True
        self._last_pretty = None
        self._entry = 'Error'

    @staticmethod
    def _decimal_to_display_string(d: Decimal) -> str:
        s = format(d, 'f')
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        if s in ('', '-'):
            s = '0'
        return s

    def _format_result_for_output(self, d: Decimal) -> str:
        try:
            exp = d.as_tuple().exponent
        except InvalidOperation:
            raise OverflowError
        if exp < 0 and -exp > 6:
            d = d.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
        return self._decimal_to_display_string(d)

    @staticmethod
    def _format_with_commas(raw: str) -> str:
        if raw == 'Error':
            return raw
        neg = raw.startswith('-')
        body = raw[1:] if neg else raw
        if '.' in body:
            int_part, frac = body.split('.', 1)
        else:
            int_part, frac = body, None
        if not int_part or int_part == '-':
            int_part = '0'
        sign_prefix = '-' if neg else ''
        j = 0
        while j < len(int_part) - 1 and int_part[j] == '0':
            j += 1
        int_part = int_part[j:]
        out = []
        for i, ch in enumerate(reversed(int_part)):
            if i and i % 3 == 0:
                out.append(',')
            out.append(ch)
        int_fmt = ''.join(reversed(out))
        if frac is not None:
            return f'{sign_prefix}{int_fmt}.{frac}'
        return f'{sign_prefix}{int_fmt}'
