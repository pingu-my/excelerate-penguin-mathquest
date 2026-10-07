"""Original generated practice templates. Fractions remain exact."""
from fractions import Fraction as F
import random
from curriculum import DIFFICULTIES

def fmt(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else str(x)

def tex(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else rf'\frac{{{x.numerator}}}{{{x.denominator}}}'

def original_base(topic, year, difficulty, rng):
    d = DIFFICULTIES.index(difficulty)
    scale = 10 ** (year - 3)
    a, b = rng.randint(2, 12), rng.randint(2, 9)
    if topic == 'Whole Numbers':
        a, b = rng.randint(scale, 9*scale), rng.randint(10, scale)
        if d == 0:
            return 'Calculate.', rf'{a}+{b}', F(a+b), 'Add by place value.', rf'{a}+{b}={a+b}'
        if d == 1:
            return 'Find the missing number.', rf'\Box+{b}={a+b}', F(a), 'Undo addition using subtraction.', rf'{a+b}-{b}={a}'
        return (f'Waddle collected {a} fish, gave away {b}, then received twice that gift. How many fish now?',
                '', F(a+b), 'Subtract the gift, then add twice the gift.', rf'{a}-{b}+2\times{b}={a+b}')
    if topic == 'Operations':
        if d == 0:
            return 'Calculate.', rf'{a}\times{b}', F(a*b), 'Use equal groups.', rf'{a}\times{b}={a*b}'
        if d == 1:
            return 'Find the missing number.', rf'\Box\div{b}={a}', F(a*b), 'Undo division using multiplication.', rf'{a}\times{b}={a*b}'
        return (f'{a} penguins each catch {b} fish. They share all the fish equally between {b} baskets. How many fish per basket?',
                '', F(a), 'Find all the fish, then divide by the number of baskets.', rf'({a}\times{b})\div{b}={a}')
    if topic == 'Fractions':
        den = rng.choice([4, 6, 8, 10, 12]); n = rng.randint(1, den-1)
        x = F(n, den)
        if d == 0:
            y = F(1, den); answer = x+y
            return 'Add the fractions.', tex(x)+'+'+tex(y), answer, 'The denominators already match.', tex(x)+'+'+tex(y)+'='+tex(answer)
        if d == 1:
            y = F(1, 2*den); answer = x+y
            return 'Add the fractions.', tex(x)+'+'+tex(y), answer, 'Use a common denominator.', tex(x)+'+'+tex(y)+'='+tex(answer)
        a *= 2  # Sharing whole fish must leave a whole-number count.
        total = den*a
        return (f'Waddle has {total} fish. He gives away {fmt(x)} of them, then half of what remains. How many fish remain?',
                '', F((den-n)*a,2), 'Find what remains after the first gift, then halve it.',
                rf'{total}\times(1-{tex(x)})\times\frac{{1}}{{2}}={tex(F((den-n)*a,2))}')
    if topic in ['Decimals', 'Money']:
        x, y = F(rng.randint(100, 5000),100), F(rng.randint(100,2000),100)
        if topic == 'Decimals' and d == 2:
            y = min(y, x*b-F(1,100))
        label = 'Give the amount in RM, without typing RM.' if topic == 'Money' else 'Calculate.'
        if d == 0:
            return label, f'{float(x):.2f}+{float(y):.2f}', x+y, 'Line up the decimal points.', f'{float(x):.2f}+{float(y):.2f}={float(x+y):.2f}'
        if d == 1:
            total = x+y
            return label, f'{float(total):.2f}-{float(y):.2f}', x, 'Subtract using place value.', f'{float(total):.2f}-{float(y):.2f}={float(x):.2f}'
        return (f'Waddle buys {b} items at {float(x):.2f} each and pays {float(x*b+y):.2f}. Find his change.' if topic == 'Money'
                else f'{b} bottles each hold {float(x):.2f} litres. Waddle uses {float(y):.2f} litres. How many litres remain?',
                '', y if topic == 'Money' else x*b-y, 'Multiply first, then subtract.',
                f'{float(x*b+y):.2f}-{b}\\times{float(x):.2f}={float(y):.2f}' if topic == 'Money' else
                f'{b}\\times{float(x):.2f}-{float(y):.2f}={float(x*b-y):.2f}')
    if topic == 'Percentages':
        p = rng.randrange(5,100,5); total = rng.randint(2,20)*20
        if d == 0:
            return 'Write the percentage as a decimal.', rf'{p}\%', F(p,100), 'Percentage means out of 100.', rf'{p}\div100={float(F(p,100))}'
        if d == 1:
            return 'Find the value.', rf'{p}\%\text{{ of }}{total}', F(p*total,100), 'Divide by 100, then multiply.', rf'\frac{{{p}}}{{100}}\times{total}={tex(F(p*total,100))}'
        ans = F(total*(100-p),100)
        return f'A bag costs RM{total}. A shop gives a {p}% discount. Find the new price in RM.', '', ans, 'Find the discount, then subtract it.', rf'{total}\times\frac{{{100-p}}}{{100}}={tex(ans)}'
    if topic == 'Time':
        h,m = rng.randint(1,12), rng.randint(1,59)
        if d == 0:
            return f'Convert {h} hours into minutes.', '', F(h*60), 'Each hour has 60 minutes.', rf'{h}\times60={h*60}'
        if d == 1:
            return f'Convert {h} hours {m} minutes into minutes.', '', F(h*60+m), 'Convert the hours, then add the extra minutes.', rf'{h}\times60+{m}={h*60+m}'
        start = rng.randint(0,22-h)*60+m; end = start+h*60+b
        return f'A trip starts at {start//60:02d}:{start%60:02d} and ends at {end//60:02d}:{end%60:02d} on the same day. How many minutes long is it?', '', F(h*60+b), 'Convert both clock times to minutes after midnight.', rf'{end}-{start}={h*60+b}'
    if topic == 'Measurement':
        x = F(a*10+b,10)
        if d == 0:
            return f'Convert {a} metres into centimetres.', '', F(a*100), '1 metre = 100 centimetres.', rf'{a}\times100={a*100}'
        if d == 1:
            return f'Convert {float(x):.1f} metres into centimetres.', '', x*100, 'Multiply metres by 100.', rf'{float(x):.1f}\times100={int(x*100)}'
        return f'A ribbon is {float(x):.1f} m long. Waddle cuts off {b} cm. How many centimetres remain?', '', x*100-b, 'Convert all lengths to the same unit first.', rf'{float(x):.1f}\times100-{b}={int(x*100-b)}'
    if topic == 'Geometry':
        if d == 0:
            return f'A rectangle is {a} cm long and {b} cm wide. Find its perimeter in cm.', '', F(2*(a+b)), 'Add all four sides.', rf'2({a}+{b})={2*(a+b)}'
        if d == 1:
            return f'A rectangle is {a} cm long and {b} cm wide. Find its area in square centimetres.', '', F(a*b), 'Area = length × width.', rf'{a}\times{b}={a*b}'
        return f'A rectangular garden is {a+b} m by {b} m. A square pond of side {b} m is inside it. Find the remaining garden area in square metres.', '', F(a*b), 'Subtract the pond area from the whole rectangle area.', rf'({a+b})\times{b}-{b}^2={a*b}'
    if topic == 'Ratio & Proportion':
        if d == 0:
            return f'Red : blue fish = {a}:{b}. There are {a*2} red fish. How many blue fish?', '', F(b*2), 'Both ratio parts grow by the same factor.', rf'{b}\times2={b*2}'
        if d == 1:
            return f'{(a+b)*3} fish are shared in the ratio {a}:{b}. How many fish are in the first share?', '', F(a*3), 'Find one part from the total number of parts.', rf'\frac{{{a}}}{{{a+b}}}\times{(a+b)*3}={a*3}'
        return f'Red : blue fish = {a}:{b}. There are {a*4} red fish. After adding {b} more blue fish, how many blue fish are there?', '', F(b*5), 'Find the original blue count, then add the extra fish.', rf'{b}\times4+{b}={b*5}'
