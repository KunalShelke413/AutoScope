
character_columns=['name', 'department', 'departments', 'team', 'teams', 'product', 'products',
 'region', 'regions', 'subject', 'subjects', 'class', 'school', 'schools',
 'assignment', 'assignments', 'age group', 'age groups', 'disease', 'diseases',
 'hospital', 'hospitals', 'city', 'cities', 'campaign', 'campaigns',
 'platform', 'platforms', 'segment', 'segments', 'ad type', 'ad types',
 'device', 'devices', 'app version', 'app versions', 'feature', 'features',
 'day', 'days', 'error type', 'error types', 'country', 'countries', 'state', 'states',
 'zone', 'zones', 'income bracket', 'income brackets', 'gender', 'genders',
 'warehouse', 'warehouses', 'category', 'categories', 'supplier', 'suppliers',
 'delivery route', 'delivery routes', 'shipment date', 'shipment dates',
 'storage section', 'storage sections', 'developer', 'developers',
 'module', 'modules', 'sprint', 'sprints', 'bug type', 'bug types',
 'task', 'tasks', 'product type', 'product types', 'payment method',
 'payment methods', 'customer', 'coupon', 'coupon codes', 'store branch',
 'store branches', 'content type', 'content types', 'influencer',
 'influencers', 'hashtag', 'hashtags', 'posting time', 'posting times',
 'audience segment', 'audience segments', 'district', 'districts',
 'scheme', 'schemes', 'utility', 'utility types', 'complaint type',
 'complaint types', 'license category', 'license categories',
 'player', 'players', 'match', 'matches', 'event', 'events',
 'training', 'exercise', 'exercises', 'sleep day', 'meal', 'meals',
 'expense category', 'expense categories', 'mood', 'book', 'books',
 'course', 'courses', 'topic', 'topics', 'quiz', 'attempt', 'instructor',
 'instructors', 'skill', 'skills', 'learning mode', 'learning modes',
 'entry', 'entries', 'journal', 'peer', 'certificate', 'certificates']

time_columns=['date', 'dates', 'time', 'times', 'timestamp', 'timestamps', 'datetime', 'datetimes','month', 'months',
              'week', 'weeks', 'day', 'days',
 'quarter', 'quarters', 'year', 'years', 'time slot', 'time slots',
 'date', 'dates', 'season', 'seasons', 'hour', 'hours',
 'posting time', 'posting times', 'training day', 'sleep day',
 'shipment date', 'shipment dates','qtr']

location_terms = {
    "country": [
        "country", "nation", "country_name", "nationality", "sovereign_state",
        "land", "homeland", "country_code", "iso_country", "nation_name",
        "odname", "dev", "world", "continent", "subcontinent", "subregion",
        "member_state", "member_country", "state_party"
    ],
    "city": [
        "city", "town", "municipality", "metro", "metropolis", "urban_area",
        "city_name", "township", "borough", "capital", "village", "urban",
        "metro_area", "conurbation", "settlement", "locality_name"
    ],
    "state": [
        "state", "province", "region", "territory", "governorate", "prefecture",
        "division", "county", "oblast", "subdivision", "federal_state", "administrative_area",
        "state_name", "province_name", "region_name", "territory_name", "governorate_name",
        "prefecture_name", "division_name", "county_name", "oblast_name",
        "state_code", "province_code", "region_code", "territory_code", "governorate_code",
        "prefecture_code", "division_code", "county_code", "oblast_code",
        "state_id", "province_id", "region_id", "territory_id", "governorate_id",
        "prefecture_id", "division_id", "county_id", "oblast_id",
        "state_abbr", "province_abbr", "region_abbr", "territory_abbr", "governorate_abbr",
        "prefecture_abbr", "division_abbr", "county_abbr", "oblast_abbr",
        "state_iso", "province_iso", "region_iso", "territory_iso", "governorate_iso",
        "prefecture_iso", "division_iso", "county_iso", "oblast_iso",
        "reg", "reg_name", "reg_code", "reg_abbr", "reg_iso", "regname",
        "statehood", "admin_region", "admin_division", "state_entity"
    ],
    "area": [
        "area", "district", "locality", "zone", "subzone", "sector",
        "ward", "neighborhood", "region_area", "block", "circle", "areaname",
        "subdistrict", "tehsil", "taluka", "parish", "commune", "borough_area"
    ],
    "postal": [
        "postal","postalcode", "postal_code", "zipcode", "zip", "pin", "pincode",
        "post_code", "mail_code", "zip_code", "postal_number", "postcode",
        "delivery_code", "sorting_code"
    ],
    "address": [
        "address", "street", "street_address", "road", "lane", "avenue", "drive",
        "colony", "apartment", "flat", "building", "house_number", "location",
        "residence", "unit", "plot", "lot", "address_line"
    ],
    "coordinates": [
        "latitude", "lat", "longitude", "lon", "lng", "geo",
        "geo_location", "coordinates", "x_coord", "y_coord", "geocode",
        "latlon", "longlat", "gps", "spatial", "geom"
    ]
}

Numerical_columns=['id','sales', 'revenue', 'growth', 'expense', 'expenses', 'count', 'counts',
 'score', 'scores', 'rating', 'ratings', 'completion', 'attendance',
 'population', 'income', 'performance', 'progress', 'conversion',
 'clicks', 'reach', 'usage', 'crashes', 'crash', 'frequency',
 'GDP', 'engagement', 'vaccinations', 'mortality', 'patients',
 'cases', 'admissions', 'footfall', 'impressions', 'views',
 'capacity', 'volume', 'stats', 'mastery', 'attempts',
 'coverage', 'distribution', 'amount', 'percent', 'percentage',
 'rate', 'rates', 'spent', 'spend', 'return', 'budget', 'budgets',
 'redemption', 'allocation', 'satisfaction', 'like', 'likes',
 'share', 'shares', 'followers', 'follower', 'reach', 'ROI',
 'usage', 'value', 'values', 'lead', 'leads', 'crashes',
 'api calls', 'downloads', 'temperature', 'transactions',
 'visits', 'visitors', 'literacy', 'energy', 'traffic',
 'restock', 'delivery', 'orders', 'stock', 'quantity',
 'damage', 'line', 'code', 'bugs', 'fixed', 'commits',
 'test coverage', 'placed', 'purchases', 'calories',
 'calorie', 'burned', 'speed', 'ranking', 'point', 'points',
 'goals', 'score', 'completed', 'attempts', 'correct',
 'answer', 'difficulty', 'duration', 'productivity',
 'usage', 'conversion', 'engagement', 'impressions','avg','average']

Contact = ["phone","phone_number","mobile","mobile_number","contact","contact_number",
           "telephone","telephone_number","cell","cell_number","phone_no","mobile_no",
           "contact_no","tel_no","primary_phone","secondary_phone","work_phone","home_phone",
           "office_phone","personal_phone","emergency_contact_number"] 

SUM_COLUMNS = [
    "amount", "total_amount", "price", "unit_price", "cost", "total_cost",
    "revenue", "sales", "net_sales", "gross_sales", "income", "profit",
    "loss", "expense", "expenses", "billing_amount", "invoice_amount",
    "payment", "paid_amount", "balance", "tax", "gst", "vat", "discount",

    "order","orders","order_value", "order_amount", "purchase_amount", "sale_amount",
    "transaction_amount", "transaction_value", "cart_value", "subtotal",
    "grand_total",

    "weight", "total_weight", "volume", "total_volume", "area",
    "distance", "total_distance",

    "score", "total_score", "marks", "total_marks", "points", "total_points",

    "time_spent", "duration", "total_time", "hours", "minutes", "seconds",

    "units_consumed", "power_consumption", "fuel_consumption",
    "electricity_units", "water_usage", "data_usage"
]

COUNT_COLUMNS= [
    "quantity", "qty", "count", "number", "ordernumber","order_number", "items", "units",
    "records", "entries", "cases", "instances", "samples",
    "observations",

    "form", "submission", "response", "application", "request",
    "complaint", "feedback",

    "signup", "registration", "login", "logout", "activity",
    "action", "interaction", "event",

    "page_view", "impression", "hit", "visit", "session",
    "bounce", "conversion", "lead",

    "error", "warning", "failure", "crash", "alert", "incident",
    "issue", "ticket",

    "attendance", "enrollment", "exam", "test", "attempt",

    "appointment", "diagnosis", "procedure", "followup",

    "cart", "order_count", "product_view", "wishlist",
    "return", "shipment", "delivery",

    "status", "flag", "label", "tag", "type", "category"
]


def get_data():
    return character_columns, time_columns, location_terms, Numerical_columns, Contact, SUM_COLUMNS, COUNT_COLUMNS