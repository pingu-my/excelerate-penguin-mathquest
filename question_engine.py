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
    if topic == 'Data Handling':
        values = [a,b,a+b]
        if d == 0:
            return f'Fish caught on three days: {a}, {b}, {a+b}. Find the total.', '', F(2*(a+b)), 'Add the three counts.', rf'{a}+{b}+{a+b}={2*(a+b)}'
        if d == 1:
            return f'Find the mean of {a}, {b}, {a+b}.', '', F(2*(a+b),3), 'Mean = total ÷ number of values. An exact fraction is accepted.', rf'({a}+{b}+{a+b})\div3={tex(F(2*(a+b),3))}'
        return f'The mean of four numbers is {a+b}. Three numbers are {a}, {b} and {a+b}. Find the fourth.', '', F(2*(a+b)), 'Find the total of all four before subtracting the three known numbers.', rf'4\times{a+b}-({a}+{b}+{a+b})={2*(a+b)}'
    if topic == 'Probability':
        red,blue = a,b
        if d == 0:
            return f'A bag has {red} red and {blue} blue counters. Find the probability of picking a red counter.', '', F(red,red+blue), 'Probability = favourable outcomes ÷ all equally likely outcomes.', rf'\frac{{{red}}}{{{red+blue}}}={tex(F(red,red+blue))}'
        if d == 1:
            return f'A bag has {red} red, {blue} blue and {red} green counters. Find the probability of NOT picking blue.', '', F(2*red,2*red+blue), 'Count the red and green counters together.', rf'\frac{{{red}+{red}}}{{{2*red+blue}}}={tex(F(2*red,2*red+blue))}'
        return f'A bag has {red} red and {blue} blue counters. Waddle adds {blue} more blue counters. Find the new probability of picking red.', '', F(red,red+2*blue), 'Update the total before finding the probability.', rf'\frac{{{red}}}{{{red}+2\times{blue}}}={tex(F(red,red+2*blue))}'
    raise ValueError(topic)


def base(topic, year, difficulty, rng, variant=0):
    """Six skill families per topic; all arithmetic uses exact fractions."""
    if variant == 0:
        return original_base(topic, year, difficulty, rng)
    d = DIFFICULTIES.index(difficulty)
    a = rng.randint(3, 12 + 6*d)
    b = rng.randint(2, 9)
    k = rng.randint(2, 5+d)
    def item(prompt, answer, hint, expression):
        answer = F(answer)
        return prompt, '', answer, hint, expression + '=' + tex(answer)
    if topic == 'Whole Numbers':
        n = rng.randint(100, 999) * (10**(year-4)) + rng.randint(0, 9)
        place = rng.choice([10, 100])
        if variant == 1:
            return item(f'In {n:,}, what is the value of the digit in the {"tens" if place == 10 else "hundreds"} place?', (n//place%10)*place, 'Identify the digit, then multiply by its place value.', rf'{n//place%10}\times{place}')
        if variant == 2:
            return item(f'Round {n:,} to the nearest {place}.', ((n+place//2)//place)*place, 'Look at the digit immediately to the right of the rounding place.', rf'\operatorname{{round}}_{{{place}}}({n})')
        if variant == 3:
            return item(f'The sequence is {a}, {a+b}, {a+2*b}, … . It increases by the same amount. Find the next term.', a+3*b, 'Find the difference between consecutive terms.', rf'{a+2*b}+{b}')
        if variant == 4:
            return item(f'Write the number with {a} hundreds, {b} tens and {k} ones.', 100*a+10*b+k, 'Add the values of the hundreds, tens and ones.', rf'{a}\times100+{b}\times10+{k}')
        return item(f'A library has {n} books. It receives {a*b} more, then lends out {a} books. How many remain?', n+a*b-a, 'Add the delivery, then subtract the loan.', rf'{n}+{a*b}-{a}')
    if topic == 'Operations':
        if variant == 1: return item(f'Share {a*b} fish equally among {b} penguins. How many does each get?', a, 'Divide the total by the number of penguins.', rf'{a*b}\div{b}')
        if variant == 2: return item(f'Calculate {a} + {b} × {k}.', a+b*k, 'Multiply before adding.', rf'{a}+{b}\times{k}')
        if variant == 3: return item(f'Find the missing number: {a} × ? = {a*b}.', b, 'Undo multiplication by dividing.', rf'{a*b}\div{a}')
        if variant == 4: return item(f'Calculate ({a} + {b}) × {k}.', (a+b)*k, 'Calculate inside the brackets first.', rf'({a}+{b})\times{k}')
        return item(f'Pack {a*b+k} biscuits into boxes of {b}. How many full boxes can be filled?', (a*b+k)//b, 'Divide and count only full boxes.', rf'\left\lfloor{a*b+k}\div{b}\right\rfloor')
    if topic == 'Fractions':
        den = rng.choice([4, 6, 8, 10, 12]); n = rng.randint(1, den-1); x = F(n,den)
        if variant == 1: return item(f'Find {fmt(x)} of {den*a}.', n*a, 'Divide by the denominator, then multiply by the numerator.', rf'{tex(x)}\times{den*a}')
        if variant == 2: return item(f'A cake is whole. Waddle eats {fmt(x)} of it. What fraction remains?', 1-x, 'Subtract the eaten fraction from one whole.', '1-'+tex(x))
        if variant == 3: return item(f'Write {a} {fmt(x)} as an improper fraction.', a+x, 'Multiply the whole number by the denominator, then add the numerator.', rf'{a}+{tex(x)}')
        if variant == 4: return item(f'Share {fmt(x)} litres equally among {k} cups. How many litres in each cup?', x/k, 'Divide the fraction by the number of cups.', rf'{tex(x)}\div{k}')
        return item(f'A recipe uses {fmt(x)} kg of flour per batch. Find the flour needed for {k} batches, in kg.', x*k, 'Multiply the amount for one batch by the number of batches.', rf'{tex(x)}\times{k}')
    if topic == 'Decimals':
        x=F(rng.randint(101,999),100)
        if variant == 1: return item(f'Write {float(x):.2f} as a fraction.', x, 'Hundredths can be written over 100 and simplified.', tex(x))
        if variant == 2: return item(f'Multiply {float(x):.2f} by {10**k}.', x*10**k, 'Each multiplication by ten shifts digits one place left.', rf'{float(x):.2f}\times{10**k}')
        if variant == 3: return item(f'Round {float(x):.2f} to one decimal place.', F((x*100+5)//10,10), 'Use the hundredths digit to decide whether to round up.', rf'\operatorname{{round}}_{{0.1}}({float(x):.2f})')
        if variant == 4: return item(f'{k} equal pieces of ribbon together measure {float(x*k):.2f} m. Find one piece in metres.', x, 'Divide the total length by the number of pieces.', rf'{float(x*k):.2f}\div{k}')
        return item(f'Find the missing decimal: ? + {float(x):.2f} = {float(x+F(b,10)):.2f}.', F(b,10), 'Subtract the known addend from the total.', rf'{float(x+F(b,10)):.2f}-{float(x):.2f}')
    if topic == 'Money':
        price=F(a*100+b*10,100)
        if variant == 1: return item(f'{k} identical notebooks cost RM{float(price*k):.2f}. Find the price of one notebook in RM.', price, 'Divide the cost by the number of notebooks.', rf'{float(price*k):.2f}\div{k}')
        if variant == 2: return item(f'Waddle saves RM{a} each week for {k} weeks. How much does he save in RM?', a*k, 'Multiply weekly savings by the number of weeks.', rf'{a}\times{k}')
        if variant == 3: return item(f'A toy costs RM{a*b}. Waddle has RM{a}. How much more does he need in RM?', a*b-a, 'Subtract his savings from the price.', rf'{a*b}-{a}')
        if variant == 4: return item(f'Convert {a*100+b} sen to RM.', F(a*100+b,100), '100 sen equals RM1.', rf'{a*100+b}\div100')
        return item(f'A ticket costs RM{a}. A group buys {k} tickets and pays a booking fee of RM{b}. Find the total cost in RM.', a*k+b, 'Multiply for the tickets, then add the fee.', rf'{a}\times{k}+{b}')
    if topic == 'Percentages':
        p=rng.choice([10,20,25,40,50,60,75,80]); total=20*a
        if variant == 1: return item(f'Write {p}/100 as a percentage. Enter the number without %.', p, 'Multiply the fraction by 100.', rf'\frac{{{p}}}{{100}}\times100')
        if variant == 2: return item(f'{p}% of the seats are occupied. What percentage is empty? Enter the number without %.', 100-p, 'The occupied and empty percentages total 100.', rf'100-{p}')
        if variant == 3: return item(f'{total} pupils attend a club. {p}% are boys. How many are girls?', F(total*(100-p),100), 'Find the percentage of girls first.', rf'{total}\times\frac{{{100-p}}}{{100}}')
        if variant == 4: return item(f'A price of RM{total} increases by {p}%. Find the new price in RM.', F(total*(100+p),100), 'Add the percentage increase to the original price.', rf'{total}\times\frac{{{100+p}}}{{100}}')
        return item(f'A test has {total} marks. A pupil earns {fmt(F(total*p,100))} marks. Find the percentage score. Enter the number without %.', p, 'Divide earned marks by total marks, then multiply by 100.', rf'{tex(F(total*p,100))}\div{total}\times100')
    if topic == 'Time':
        if variant == 1: return item(f'Convert {a} minutes {b} seconds into seconds.', a*60+b, 'There are 60 seconds in a minute.', rf'{a}\times60+{b}')
        if variant == 2: return item(f'Waddle studies for {a*b} minutes and rests for {b} minutes. Find the total time in minutes.', a*b+b, 'Add study time and rest time.', rf'{a*b}+{b}')
        if variant == 3: return item(f'Waddle has {a*60} minutes available. Each lesson takes {b*5} minutes. How many complete lessons fit?', a*60//(b*5), 'Divide available time by lesson time; count full lessons.', rf'\left\lfloor{a*60}\div{b*5}\right\rfloor')
        if variant == 4: return item(f'A trip lasts {a*b} minutes, including a {b}-minute stop. How many minutes are spent travelling?', a*b-b, 'Remove the stop time from the total.', rf'{a*b}-{b}')
        return item(f'A timer counts {a*60} seconds. How many minutes is this?', a, 'Divide the seconds by 60.', rf'{a*60}\div60')
    if topic == 'Measurement':
        if variant == 1: return item(f'Convert {a} kg {b*10} g into grams.', a*1000+b*10, '1 kg equals 1000 g.', rf'{a}\times1000+{b*10}')
        if variant == 2: return item(f'Convert {a} litres {b*10} ml into millilitres.', a*1000+b*10, '1 litre equals 1000 ml.', rf'{a}\times1000+{b*10}')
        if variant == 3: return item(f'Share {a*k} cm of ribbon into {k} equal pieces. Find each length in cm.', a, 'Divide the total length by the number of pieces.', rf'{a*k}\div{k}')
        if variant == 4: return item(f'A bag weighs {a*100} g and another weighs {b*100} g. Find their combined mass in kg.', F(a+b,10), 'Add grams, then divide by 1000.', rf'({a*100}+{b*100})\div1000')
        return item(f'A bottle holds {a*100} ml. {b*10} ml is poured out. How many millilitres remain?', a*100-b*10, 'Subtract the poured amount from the starting amount.', rf'{a*100}-{b*10}')
    if topic == 'Geometry':
        if variant == 1: return item(f'A square has side {a} cm. Find its perimeter in cm.', 4*a, 'A square has four equal sides.', rf'4\times{a}')
        if variant == 2: return item(f'A rectangle has area {a*b} square cm and width {b} cm. Find its length in cm.', a, 'Divide area by width.', rf'{a*b}\div{b}')
        if variant == 3: return item(f'Two angles on a straight line are {a*5}° and another angle. Find the other angle in degrees.', 180-a*5, 'Angles on a straight line add to 180 degrees.', rf'180-{a*5}')
        if variant == 4: return item(f'A triangle has angles {a*3}° and {b*5}°. Find the third angle in degrees.', 180-a*3-b*5, 'The three angles of a triangle total 180 degrees.', rf'180-{a*3}-{b*5}')
        return item(f'A rectangle has perimeter {2*(a+b)} cm and length {a} cm. Find its width in cm.', b, 'Halve the perimeter, then subtract the length.', rf'{2*(a+b)}\div2-{a}')
    if topic == 'Ratio & Proportion':
        if variant == 1: return item(f'A recipe serves {k} people and uses {a*k} g of rice. How much rice serves {k+1} people, in grams?', a*(k+1), 'Find rice for one person, then scale up.', rf'{a*k}\div{k}\times{k+1}')
        if variant == 2: return item(f'{k} identical pens cost RM{a*k}. Find the cost of {b} pens in RM.', a*b, 'Find the unit price, then multiply.', rf'{a*k}\div{k}\times{b}')
        if variant == 3: return item(f'Red : blue counters = {a}:{b}. There are {b*k} blue counters. How many counters altogether?', (a+b)*k, 'Find the scale factor using the blue counters.', rf'({a}+{b})\times{k}')
        if variant == 4: return item(f'{(a+b)*k} sweets are shared in the ratio {a}:{b}. Find the second share.', b*k, 'Find one ratio part, then multiply by the second part.', rf'{(a+b)*k}\div{a+b}\times{b}')
        return item(f'A map uses 1 cm for {k} km. Two towns are {a} cm apart on the map. Find the real distance in km.', a*k, 'Multiply map distance by kilometres per centimetre.', rf'{a}\times{k}')
    if topic == 'Data Handling':
        vals=[a,b,a+b,a+k,b+k]
        if variant == 1: return item(f'Find the range of these values: {", ".join(map(str,vals))}.', max(vals)-min(vals), 'Range is the largest value minus the smallest.', rf'{max(vals)}-{min(vals)}')
        if variant == 2: return item(f'Find the median of these five values: {", ".join(map(str,vals))}.', sorted(vals)[2], 'Sort all five values; choose the middle value.', rf'\operatorname{{median}}({",".join(map(str,sorted(vals)))})')
        if variant == 3: return item(f'Find the mode of {a}, {b}, {a}, {a+b}, {a}.', a, 'The mode occurs most often.', rf'\operatorname{{mode}}({a},{b},{a},{a+b},{a})')
        if variant == 4: return item(f'A table shows {a*k} votes for skating and {b*k} for swimming. How many more votes does the more popular activity have?', abs(a-b)*k, 'Subtract the smaller frequency from the larger.', rf'{max(a,b)*k}-{min(a,b)*k}')
        return item(f'The mean of {k} numbers is {a}. Find their total.', a*k, 'Total equals mean times number of values.', rf'{a}\times{k}')
    if topic == 'Probability':
        sides=rng.choice([6,8,10,12]); cut=rng.randint(2,sides-1)
        if variant == 1: return item(f'A fair spinner has equally sized sections numbered 1 to {sides}. Find the probability of an even number.', F(1,2), 'Count the even sections and divide by all sections.', rf'\frac{{{sides//2}}}{{{sides}}}')
        if variant == 2: return item(f'A fair spinner has equally sized sections numbered 1 to {sides}. Find the probability of a number greater than {cut}.', F(sides-cut,sides), 'Count only the numbers above the given number.', rf'\frac{{{sides-cut}}}{{{sides}}}')
        if variant == 3: return item(f'A bag has {a} red and {b} blue counters. Find the probability of NOT picking red.', F(b,a+b), 'Count the blue counters as the favourable outcomes.', rf'\frac{{{b}}}{{{a+b}}}')
        if variant == 4: return item(f'A bag has {a} red and {b} blue counters. {b-1} blue counters are removed. Find the new probability of picking red.', F(a,a+1), 'Update the remaining counters before calculating.', rf'\frac{{{a}}}{{{a}+1}}')
        return item(f'A fair spinner has equally sized sections numbered 1 to {sides}. Find the probability of a number at most {cut}.', F(cut,sides), 'Include the given number when counting favourable sections.', rf'\frac{{{cut}}}{{{sides}}}')
    raise ValueError(topic)


def make_question(topic, year, difficulty, kind, rng, uid, variant=0):
    instruction, latex, answer, hint, solution = base(topic, year, difficulty, rng, variant)
    q = dict(id=uid, difficulty=difficulty, question_type=kind, skill_variant=variant,
             instruction=instruction, latex=latex, answer=fmt(answer),
             hints=[hint, 'Write the known values and keep all units consistent.',
                    'Use the rule in the first hint, then check the answer against the question.'], solution=solution)
    if kind == 'mcq':
        step = F(1,10) if answer.denominator != 1 else F(1)
        candidates = {answer + step, answer - step, answer*2, answer/2, answer+2*step, answer-2*step}
        if topic == 'Probability':
            candidates = {F(n,12) for n in range(13)}
        candidates.discard(answer)
        options = [answer] + rng.sample(sorted(candidates), 3)
        rng.shuffle(options)
        q['options'] = [fmt(x) for x in options]
    elif kind in ['matching', 'drag_drop']:
        # Use one skill within a group so ordered answers have consistent units.
        entries = [(instruction,latex,answer,solution)]
        group_variant = variant
        if topic == 'Probability' and variant == 1:
            group_variant = 2  # Even-number probabilities are always one half.
            entries = []
        for _ in range(500):
            if len(entries) == 3: break
            candidate = base(topic,year,difficulty,rng,group_variant)
            if candidate[2] not in [v[2] for v in entries]:
                entries.append((candidate[0],candidate[1],candidate[2],candidate[4]))
        if len(entries) != 3:
            raise RuntimeError('Could not generate three distinct group answers')
        q['latex'] = ''
        if kind == 'matching':
            q['instruction'] = 'Match each problem to its answer. Use each answer once.'
            q['pairs'] = [dict(prompt=v[0],latex=v[1],answer=fmt(v[2]),solution=v[3]) for v in entries]
            q['options'] = [v['answer'] for v in q['pairs']]; rng.shuffle(q['options'])
        else:
            q['instruction'] = 'Solve A, B and C, then drag their cards from smallest answer to largest.'
            q['problems'] = [dict(label=chr(65+i),prompt=v[0],latex=v[1],answer=fmt(v[2]),solution=v[3]) for i,v in enumerate(entries)]
            q['answer'] = [chr(65+i) for i in sorted(range(3),key=lambda i:entries[i][2])]
            q['cards'] = ['A','B','C']; rng.shuffle(q['cards'])
    return q


def build_adventure(year, syllabus, topic, mode, seed=None):
    rng = random.Random(seed)
    levels = DIFFICULTIES if mode == 'All three levels' else [mode]
    kinds = ['numeric','mcq','matching','numeric','drag_drop','mcq','numeric','matching','drag_drop','numeric']
    questions=[]; signatures=set()
    for difficulty in levels:
        # Each of the six individual questions uses a different skill family.
        variants=list(range(6)); rng.shuffle(variants)
        singles=iter(variants)
        for index,kind in enumerate(kinds):
            variant=next(singles) if kind in ['numeric','mcq'] else rng.randrange(6)
            for _ in range(200):
                q=make_question(topic,year,difficulty,kind,rng,f'{difficulty}-{index}',variant)
                signature=repr((q['instruction'],q['latex'],q.get('pairs'),q.get('problems')))
                if signature not in signatures:
                    signatures.add(signature);questions.append(q);break
            else: raise RuntimeError('Could not generate enough distinct questions')
    return questions
