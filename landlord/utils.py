

def get_ua_month_value(eng_month):
    months = {
        "january": "Січень",
        "february": "Лютий",
        "march": "Березень",
        "april": "Квітень",
        "may": "Травень",
        "june": "Червень",
        "july": "Липень",
        "august": "Серпень",
        "september": "Вересень",
        "october": "Жовтень",
        "november": "Листопад",
        "december": "Грудень",
    }
    return months.get(eng_month, "Місяць")