from django import template
register = template.Library() 

def numberToWords(num):
    ones = [
        "Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"
    ]
    teens = [
        "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"
    ]
    tens = [
        "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"
    ]

    if num == 0:
        return ones[0]

    words = []

    # Thousands
    thousands = num // 1000
    if thousands > 0:
        words.append(ones[thousands])
        words.append("Thousand")

    # Hundreds
    hundreds = (num // 100) % 10
    if hundreds > 0:
        words.append(ones[hundreds])
        words.append("Hundred")
        if num % 100 != 0:
            words.append("and")

    # Tens and Ones
    tens_ones = num % 100
    if tens_ones >= 11 and tens_ones <= 19:
        words.append(teens[tens_ones - 11])
    else:
        tens_digit = tens_ones // 10
        if tens_digit > 0:
            words.append(tens[tens_digit - 1])
            if num % 10 != 0:
                words.append("and")

        ones_digit = tens_ones % 10
        if ones_digit > 0:
            words.append(ones[ones_digit])

    return ' Rs. ' + " ".join(words) + ' Only'





@register.filter
def index(indexable, i):
    print(type(indexable[i].date))
    return indexable[i].date

@register.filter
def check(obj):
    if obj.total_fees==obj.collection:
        return 0 
    return 1

@register.filter
def amount_to_words(obj):
    print(obj.total_fees)
    return numberToWords(obj.total_fees)