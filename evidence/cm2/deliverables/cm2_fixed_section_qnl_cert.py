#!/usr/bin/env python3
"""Exact jet and projective certificates for fixed-section pilot orbits."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial


DEGREE = 3


def frac(value: int | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


@dataclass(frozen=True)
class Qsqrt2:
    rational: Fraction = Fraction(0)
    radical: Fraction = Fraction(0)

    def __init__(
        self,
        rational: int | Fraction = 0,
        radical: int | Fraction = 0,
    ) -> None:
        object.__setattr__(self, "rational", frac(rational))
        object.__setattr__(self, "radical", frac(radical))

    @staticmethod
    def coerce(value: int | Fraction | Qsqrt2) -> Qsqrt2:
        return value if isinstance(value, Qsqrt2) else Qsqrt2(value)

    def __add__(self, other: int | Fraction | Qsqrt2) -> Qsqrt2:
        other = self.coerce(other)
        return Qsqrt2(
            self.rational + other.rational,
            self.radical + other.radical,
        )

    __radd__ = __add__

    def __neg__(self) -> Qsqrt2:
        return Qsqrt2(-self.rational, -self.radical)

    def __sub__(self, other: int | Fraction | Qsqrt2) -> Qsqrt2:
        return self + (-self.coerce(other))

    def __rsub__(self, other: int | Fraction | Qsqrt2) -> Qsqrt2:
        return self.coerce(other) - self

    def __mul__(self, other: int | Fraction | Qsqrt2) -> Qsqrt2:
        other = self.coerce(other)
        return Qsqrt2(
            self.rational * other.rational
            + 2 * self.radical * other.radical,
            self.rational * other.radical
            + self.radical * other.rational,
        )

    __rmul__ = __mul__

    def inverse(self) -> Qsqrt2:
        norm = self.rational**2 - 2 * self.radical**2
        if norm == 0:
            raise ZeroDivisionError("zero divisor in Q(sqrt(2))")
        return Qsqrt2(self.rational / norm, -self.radical / norm)

    def __truediv__(self, other: int | Fraction | Qsqrt2) -> Qsqrt2:
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other: int | Fraction | Qsqrt2) -> Qsqrt2:
        return self.coerce(other) / self

    def __pow__(self, exponent: int) -> Qsqrt2:
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        result = Qsqrt2(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result *= base
            base *= base
            power >>= 1
        return result

    def __str__(self) -> str:
        if self.radical == 0:
            return str(self.rational)
        return f"({self.rational}) + ({self.radical})*sqrt(2)"


EXTENSION_SQUARE = Qsqrt2(0)


@dataclass(frozen=True)
class EigenExtension:
    base: Qsqrt2 = Qsqrt2(0)
    eigen: Qsqrt2 = Qsqrt2(0)

    @staticmethod
    def coerce(
        value: int | Fraction | Qsqrt2 | EigenExtension,
    ) -> EigenExtension:
        if isinstance(value, EigenExtension):
            return value
        return EigenExtension(Qsqrt2.coerce(value), Qsqrt2(0))

    def __add__(
        self,
        other: int | Fraction | Qsqrt2 | EigenExtension,
    ) -> EigenExtension:
        other = self.coerce(other)
        return EigenExtension(self.base + other.base, self.eigen + other.eigen)

    __radd__ = __add__

    def __neg__(self) -> EigenExtension:
        return EigenExtension(-self.base, -self.eigen)

    def __sub__(
        self,
        other: int | Fraction | Qsqrt2 | EigenExtension,
    ) -> EigenExtension:
        return self + (-self.coerce(other))

    def __rsub__(
        self,
        other: int | Fraction | Qsqrt2 | EigenExtension,
    ) -> EigenExtension:
        return self.coerce(other) - self

    def __mul__(
        self,
        other: int | Fraction | Qsqrt2 | EigenExtension,
    ) -> EigenExtension:
        other = self.coerce(other)
        return EigenExtension(
            self.base * other.base
            + self.eigen * other.eigen * EXTENSION_SQUARE,
            self.base * other.eigen + self.eigen * other.base,
        )

    __rmul__ = __mul__

    def inverse(self) -> EigenExtension:
        norm = self.base**2 - self.eigen**2 * EXTENSION_SQUARE
        if norm == Qsqrt2(0):
            raise ZeroDivisionError("zero divisor in eigenvalue extension")
        return EigenExtension(self.base / norm, -self.eigen / norm)

    def __truediv__(
        self,
        other: int | Fraction | Qsqrt2 | EigenExtension,
    ) -> EigenExtension:
        return self * self.coerce(other).inverse()

    def __rtruediv__(
        self,
        other: int | Fraction | Qsqrt2 | EigenExtension,
    ) -> EigenExtension:
        return self.coerce(other) / self

    def __pow__(self, exponent: int) -> EigenExtension:
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        result = EigenExtension.coerce(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result *= base
            base *= base
            power >>= 1
        return result

    def __str__(self) -> str:
        if self.eigen == Qsqrt2(0):
            return str(self.base)
        return f"({self.base}) + ({self.eigen})*q"


class Polynomial:
    def __init__(self, terms: dict[tuple[int, int], object] | None = None) -> None:
        self.terms = {
            degree: coefficient
            for degree, coefficient in (terms or {}).items()
            if sum(degree) <= DEGREE and coefficient != 0
        }

    @classmethod
    def constant(cls, value: object) -> Polynomial:
        return cls({(0, 0): value}) if value != 0 else cls()

    @classmethod
    def variable(cls, index: int, one: object) -> Polynomial:
        degree = (1, 0) if index == 0 else (0, 1)
        return cls({degree: one})

    def coefficient(self, degree: tuple[int, int], zero: object) -> object:
        return self.terms.get(degree, zero)

    def __add__(self, other: Polynomial) -> Polynomial:
        terms = dict(self.terms)
        for degree, coefficient in other.terms.items():
            terms[degree] = terms.get(degree, 0) + coefficient
        return Polynomial(terms)

    def __neg__(self) -> Polynomial:
        return Polynomial({degree: -coefficient for degree, coefficient in self.terms.items()})

    def __sub__(self, other: Polynomial) -> Polynomial:
        return self + (-other)

    def __mul__(self, other: Polynomial) -> Polynomial:
        terms: dict[tuple[int, int], object] = {}
        for (left_x, left_y), left_coefficient in self.terms.items():
            for (right_x, right_y), right_coefficient in other.terms.items():
                degree = (left_x + right_x, left_y + right_y)
                if sum(degree) <= DEGREE:
                    terms[degree] = (
                        terms.get(degree, 0)
                        + left_coefficient * right_coefficient
                    )
        return Polynomial(terms)

    def scale(self, scalar: object) -> Polynomial:
        return Polynomial(
            {degree: scalar * coefficient for degree, coefficient in self.terms.items()}
        )

    def __pow__(self, exponent: int) -> Polynomial:
        if exponent < 0:
            raise ValueError("polynomial powers must be nonnegative")
        if exponent == 0:
            if not self.terms:
                raise ValueError("cannot infer scalar one from zero polynomial")
            sample = next(iter(self.terms.values()))
            return Polynomial.constant(sample / sample)
        result = self
        for _ in range(1, exponent):
            result *= self
        return result


def constant_part(polynomial: Polynomial, zero: object) -> object:
    return polynomial.coefficient((0, 0), zero)


def square_root(polynomial: Polynomial, root: object, zero: object) -> Polynomial:
    constant = Polynomial.constant(root * root)
    remainder = polynomial - constant
    return (
        Polynomial.constant(root)
        + remainder.scale(1 / (2 * root))
        - (remainder * remainder).scale(1 / (8 * root**3))
        + (remainder * remainder * remainder).scale(1 / (16 * root**5))
    )


def inverse(polynomial: Polynomial, zero: object) -> Polynomial:
    constant = constant_part(polynomial, zero)
    remainder = polynomial - Polynomial.constant(constant)
    normalized = remainder.scale(1 / constant)
    return (
        Polynomial.constant(1 / constant)
        - normalized.scale(1 / constant)
        + (normalized * normalized).scale(1 / constant)
        - (normalized * normalized * normalized).scale(1 / constant)
    )


def quotient(numerator: Polynomial, denominator: Polynomial, zero: object) -> Polynomial:
    return numerator * inverse(denominator, zero)


def dot(left: tuple[Polynomial, Polynomial], right: tuple[Polynomial, Polynomial]) -> Polynomial:
    return left[0] * right[0] + left[1] * right[1]


def substitute(
    polynomial: Polynomial,
    first: Polynomial,
    second: Polynomial,
) -> Polynomial:
    result = Polynomial()
    one = next(iter(first.terms.values()))
    for (first_degree, second_degree), coefficient in polynomial.terms.items():
        first_power = Polynomial.constant(one / one) if first_degree == 0 else first**first_degree
        second_power = Polynomial.constant(one / one) if second_degree == 0 else second**second_degree
        result += (first_power * second_power).scale(coefficient)
    return result


def derivative(
    polynomial: Polynomial,
    first_degree: int,
    second_degree: int,
    zero: object,
) -> object:
    coefficient = polynomial.coefficient((first_degree, second_degree), zero)
    return factorial(first_degree) * factorial(second_degree) * coefficient


def collide(
    position: tuple[Polynomial, Polynomial],
    velocity: tuple[Polynomial, Polynomial],
    center: tuple[Qsqrt2, Qsqrt2],
    radius: Qsqrt2,
) -> tuple[tuple[Polynomial, Polynomial], tuple[Polynomial, Polynomial]]:
    zero = Qsqrt2(0)
    displacement = (
        position[0] - Polynomial.constant(center[0]),
        position[1] - Polynomial.constant(center[1]),
    )
    linear = dot(displacement, velocity)
    offset = dot(displacement, displacement) - Polynomial.constant(radius**2)
    discriminant = linear * linear - offset
    flight = -linear - square_root(discriminant, radius, zero)
    impact = (
        position[0] + flight * velocity[0],
        position[1] + flight * velocity[1],
    )
    normal = (
        (impact[0] - Polynomial.constant(center[0])).scale(1 / radius),
        (impact[1] - Polynomial.constant(center[1])).scale(1 / radius),
    )
    normal_speed = dot(velocity, normal)
    reflected = (
        velocity[0] - (normal_speed * normal[0]).scale(2),
        velocity[1] - (normal_speed * normal[1]).scale(2),
    )
    return impact, reflected


def convert(polynomial: Polynomial) -> Polynomial:
    return Polynomial(
        {
            degree: EigenExtension.coerce(coefficient)
            for degree, coefficient in polynomial.terms.items()
        }
    )


def normal_cycle_linear_return(
    source_radius: Qsqrt2,
    target_radius: Qsqrt2,
    center_distance: Qsqrt2,
) -> tuple[Qsqrt2, Qsqrt2, Qsqrt2, Qsqrt2]:
    zero = Qsqrt2(0)
    one = Qsqrt2(1)
    arclength = Polynomial.variable(0, one)
    momentum = Polynomial.variable(1, one)
    angle = arclength.scale(1 / source_radius)
    cosine = Polynomial.constant(one) - (angle * angle).scale(Fraction(1, 2))
    sine = angle - (angle * angle * angle).scale(Fraction(1, 6))
    normal = (cosine, sine)
    tangent = (-sine, cosine)
    cosine_phi = Polynomial.constant(one) - (momentum * momentum).scale(Fraction(1, 2))
    velocity = (
        cosine_phi * normal[0] + momentum * tangent[0],
        cosine_phi * normal[1] + momentum * tangent[1],
    )
    position = (
        normal[0].scale(source_radius),
        normal[1].scale(source_radius),
    )
    target_position, target_velocity = collide(
        position,
        velocity,
        (center_distance, zero),
        target_radius,
    )
    source_position, source_velocity = collide(
        target_position,
        target_velocity,
        (zero, zero),
        source_radius,
    )
    source_normal = (
        source_position[0].scale(1 / source_radius),
        source_position[1].scale(1 / source_radius),
    )
    slope = quotient(source_normal[1], source_normal[0], zero)
    output_angle = slope - (slope * slope * slope).scale(Fraction(1, 3))
    output_arclength = output_angle.scale(source_radius)
    source_tangent = (-source_normal[1], source_normal[0])
    output_momentum = dot(source_velocity, source_tangent)
    return (
        derivative(output_arclength, 1, 0, zero),
        derivative(output_arclength, 0, 1, zero),
        derivative(output_momentum, 1, 0, zero),
        derivative(output_momentum, 0, 1, zero),
    )


def main() -> None:
    global EXTENSION_SQUARE

    zero = Qsqrt2(0)
    one = Qsqrt2(1)
    gray_radius = Qsqrt2(Fraction(9, 25))
    white_radius = Qsqrt2(Fraction(4, 25))
    center_distance = Qsqrt2(0, Fraction(1, 2))

    arclength = Polynomial.variable(0, one)
    momentum = Polynomial.variable(1, one)
    angle = arclength.scale(1 / gray_radius)
    cosine = Polynomial.constant(one) - (angle * angle).scale(Fraction(1, 2))
    sine = angle - (angle * angle * angle).scale(Fraction(1, 6))
    normal = (cosine, sine)
    tangent = (-sine, cosine)
    cosine_phi = Polynomial.constant(one) - (momentum * momentum).scale(Fraction(1, 2))
    velocity = (
        cosine_phi * normal[0] + momentum * tangent[0],
        cosine_phi * normal[1] + momentum * tangent[1],
    )
    position = (normal[0].scale(gray_radius), normal[1].scale(gray_radius))

    white_position, white_velocity = collide(
        position,
        velocity,
        (center_distance, zero),
        white_radius,
    )
    gray_position, gray_velocity = collide(
        white_position,
        white_velocity,
        (zero, zero),
        gray_radius,
    )
    gray_normal = (
        gray_position[0].scale(1 / gray_radius),
        gray_position[1].scale(1 / gray_radius),
    )
    slope = quotient(gray_normal[1], gray_normal[0], zero)
    output_angle = slope - (slope * slope * slope).scale(Fraction(1, 3))
    output_arclength = output_angle.scale(gray_radius)
    gray_tangent = (-gray_normal[1], gray_normal[0])
    output_momentum = dot(gray_velocity, gray_tangent)

    matrix_a = derivative(output_arclength, 1, 0, zero)
    matrix_b = derivative(output_arclength, 0, 1, zero)
    matrix_c = derivative(output_momentum, 1, 0, zero)
    matrix_d = derivative(output_momentum, 0, 1, zero)
    expected_a = Qsqrt2(Fraction(661, 36), Fraction(-325, 36))
    expected_b = Qsqrt2(Fraction(859, 100), Fraction(-11, 2))
    expected_c = Qsqrt2(Fraction(15625, 324), Fraction(-625, 81))
    assert (matrix_a, matrix_b, matrix_c, matrix_d) == (
        expected_a,
        expected_b,
        expected_c,
        expected_a,
    )
    assert matrix_a**2 - matrix_b * matrix_c == one

    gray_matrix = normal_cycle_linear_return(
        gray_radius,
        gray_radius,
        Qsqrt2(1),
    )
    expected_gray_matrix = (
        Qsqrt2(Fraction(431, 81)),
        Qsqrt2(Fraction(224, 225)),
        Qsqrt2(Fraction(20000, 729)),
        Qsqrt2(Fraction(431, 81)),
    )
    assert gray_matrix == expected_gray_matrix
    assert gray_matrix[0] * gray_matrix[3] - gray_matrix[1] * gray_matrix[2] == one
    eigenline_obstruction = matrix_c * gray_matrix[1] - gray_matrix[2] * matrix_b
    expected_eigenline_obstruction = Qsqrt2(
        Fraction(-15200, 81),
        Fraction(11600, 81),
    )
    assert eigenline_obstruction == expected_eigenline_obstruction
    assert eigenline_obstruction != zero

    EXTENSION_SQUARE = matrix_b * matrix_c
    eigen_root = EigenExtension(Qsqrt2(0), Qsqrt2(1))
    adapted_ratio = eigen_root / matrix_c
    unstable = EigenExtension.coerce(matrix_a) + eigen_root
    stable = EigenExtension.coerce(matrix_a) - eigen_root

    first = Polynomial.variable(0, EigenExtension.coerce(1))
    second = Polynomial.variable(1, EigenExtension.coerce(1))
    original_arclength = first - second.scale(adapted_ratio / 2)
    original_momentum = first.scale(1 / adapted_ratio) + second.scale(Fraction(1, 2))
    transformed_arclength = substitute(
        convert(output_arclength),
        original_arclength,
        original_momentum,
    )
    transformed_momentum = substitute(
        convert(output_momentum),
        original_arclength,
        original_momentum,
    )
    unstable_output = transformed_arclength.scale(Fraction(1, 2)) + transformed_momentum.scale(
        adapted_ratio / 2
    )
    stable_output = transformed_momentum - transformed_arclength.scale(1 / adapted_ratio)
    unstable_xxx = derivative(unstable_output, 3, 0, EigenExtension.coerce(0))
    stable_xyy = derivative(stable_output, 1, 2, EigenExtension.coerce(0))
    anosov_cocycle = stable_xyy / stable
    unstable_log_jacobian_second = unstable_xxx / unstable

    assert derivative(unstable_output, 1, 0, EigenExtension.coerce(0)) == unstable
    assert (
        derivative(unstable_output, 0, 1, EigenExtension.coerce(0))
        == EigenExtension.coerce(0)
    )
    assert (
        derivative(stable_output, 1, 0, EigenExtension.coerce(0))
        == EigenExtension.coerce(0)
    )
    assert derivative(stable_output, 0, 1, EigenExtension.coerce(0)) == stable
    assert unstable_xxx != EigenExtension.coerce(0)
    assert unstable_log_jacobian_second != EigenExtension.coerce(0)
    assert anosov_cocycle == EigenExtension.coerce(Fraction(-325, 72))
    assert 72 * anosov_cocycle + 325 == EigenExtension.coerce(0)

    print("fixed-section gray--white normal cycle: CERTIFIED")
    print(f"a={matrix_a}")
    print(f"b={matrix_b}")
    print(f"c={matrix_c}")
    print(f"determinant={matrix_a**2 - matrix_b * matrix_c}")
    print(f"unstable_eigenvalue={unstable}")
    print(f"stable_eigenvalue={stable}")
    print(f"F_xxx={unstable_xxx}")
    print(f"unstable_log_J_second={unstable_log_jacobian_second}")
    print(f"G_xyy={stable_xyy}")
    print(f"Anosov_cocycle={anosov_cocycle}")
    print("fixed-section horizontal gray--gray cycle: CERTIFIED")
    print(f"gray_gray_a={gray_matrix[0]}")
    print(f"gray_gray_b={gray_matrix[1]}")
    print(f"gray_gray_c={gray_matrix[2]}")
    print(
        "gray_gray_determinant="
        f"{gray_matrix[0] * gray_matrix[3] - gray_matrix[1] * gray_matrix[2]}"
    )
    print(f"eigenline_obstruction={eigenline_obstruction}")


if __name__ == "__main__":
    main()
