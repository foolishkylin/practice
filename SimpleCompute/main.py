"""
    the main function for sc
"""
import numpy as np
import fractions
import decimal
def generate_equation(erange=10):
    """

    :param erange: the range of number in equation
    :return:
    """
    if erange < 2:
        print('the range of equation is too small')
        return ''
    operator = [' + ', ' - ', ' × ', ' ÷ ']
    end_opt = ' ='
    nnature, nfraction = np.random.randint(1, 3, size=2)
    # the sum of nature and fraction is not more than 4
    lnature = [str(x) for x in np.random.randint(1, erange, size=nnature)]
    lfloat = [str(round(x+0.5, 1)) for x in np.random.rand(nnature) * (erange / 3)]
    # add 0.5 to avoid the num is 0
    lfraction = list()
    for fraction in [fractions.Fraction(decimal.Decimal(x)) for x in lfloat]:
        lfraction.append(FfractoTfrac(fraction))
    equation = ''
    bag = lnature + lfraction
    len_bag = len(bag)
    for it in range(len_bag):
        randint = np.random.randint(len(bag))
        equation += bag[randint]
        # randomly choose the number in the bag
        if it < len_bag - 1:
            equation += operator[randint % len(operator)]
        else:
            equation += end_opt
        bag.pop(randint)
    return equation

def compute_equation(equation):
    """

    :param equation: the str of equation such as '1 + 2 ='
    :return: the answer of equation in str fomat
    """
    lequation = equation.split(' ')
    for it in range(len(lequation)):
        # fomat the equation to eval()
        etype = elem_type_judge(lequation[it])
        if etype is 'f':
            if '`' in lequation[it]:
                tnum, frac = lequation[it].split('`')
                lequation[it]= '({} + fractions.Fraction(\'{}\'))'.format(tnum, frac)
            else:
                lequation[it] = 'fractions.Fraction(\'{}\')'.format(lequation[it])
        if etype is 'n':
            lequation[it] = 'fractions.Fraction(\'{}\')'.format(lequation[it])
        elif etype is 'o': # ×
            if lequation[it] is '÷':
                lequation[it] = '/'
            if lequation[it] is '×':
                lequation[it] = '*'
        elif etype is 'e':
            lequation[it] = ''
    fequation = ''.join(lequation)
    try:
        result = eval(fequation)
        if result < 0:
            return '-1'
        else:
            return FfractoTfrac(result)
    except ValueError:
        print('the equation is wrong')
        return -1

def elem_type_judge(elem):
    """

    :param elem: a str such as '1/2'
    :return: the type of elem, such as 'f' meaning fraction
    """
    if type(elem) != str:
        raise TypeError
    if '/' in elem or '`' in elem:
        return 'f'
    elif elem in ['+', '-', '×', '÷']:
        return 'o'
    elif elem is '=':
        return 'e'
    elif elem.isdigit():
        return 'n'
    else:
        print(elem)
        raise ValueError

def FfractoTfrac(fraction):
    """
    fomat the fraction
    :param fraction:
    :return:
    """
    if fraction.numerator > fraction.denominator:
        mixed = fraction.numerator // fraction.denominator
        if fraction - mixed == 0:
            frac_str = '{}'.format(mixed)
        else:
            frac_str = '{}`{}'.format(mixed, fraction - mixed)
    else:
        frac_str = str(fraction)
    return frac_str

def generate_to_file(q_num=10, erange=10):
    """

    :param q_num: the num of quation
    :param erange: the range of quation
    :return:
    """
    q_list = list()
    a_list = list()
    cnt = 0
    while cnt < q_num:
        equation = generate_equation(erange=erange)
        answer = compute_equation(equation)
        if answer != '-1':
            q_list.append(equation)
            a_list.append(answer)
            cnt += 1
    for lt, name in zip([q_list, a_list], ['Exercises.txt', 'Answers.txt']):
        with open(name, 'w') as f:
            for row in lt:
                f.write(row)
                f.write('\n')
            f.close()

def proofreading(qf='Exercises.txt', af='Answers.txt'):
    """

    :param qf: the filename of quation
    :param af: the filename of answer
    :return:
    """
    q_list, a_list = [list(), list()]
    for lt, name in zip([q_list, a_list], [qf, af]):
        with open(name) as f:
            for line in f.readlines():
                lt.append(line.strip())
    ita = min(len(q_list), len(a_list))
    proof = {'Correct':list(), 'Wrong':list()}
    for it in range(ita):
        if compute_equation(q_list[it]) == a_list[it]:
            proof['Correct'].append(it+1)
        else:
            proof['Wrong'].append(it+1)

    file_str = 'Correct: {} {}\nWrong: {} {}'.format(
        len(proof['Correct']), str(proof['Correct']),
        len(proof['Wrong']), str(proof['Wrong']))
    with open('Grade.txt', 'w') as f:
        f.write(file_str)
        f.close()


if __name__ == '__main__':
    generate_to_file()
    proofreading()

