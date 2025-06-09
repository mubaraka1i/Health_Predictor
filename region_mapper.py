def map_country_to_macroregion(country):
    country = str(country).lower()
    if any(c in country for c in [
        "united states of america", "canada", "united kingdom", "ireland", "australia", "new zealand",
        "portugal", "spain", "france", "germany", "italy", "switzerland", "netherlands", "belgium",
        "austria", "luxembourg", "sweden", "norway", "denmark", "finland", "iceland", "czech republic",
        "slovakia", "poland", "hungary", "slovenia", "croatia", "bosnia", "serbia", "montenegro",
        "north macedonia", "greece", "bulgaria", "romania", "lithuania", "latvia", "estonia",
        "russia", "ukraine", "belarus", "georgia", "armenia"
    ]):
        return "North & Australasia"
    elif any(c in country for c in [
        "mexico", "colombia", "peru", "venezuela", "guatemala", "ecuador", "dominican republic",
        "honduras", "nicaragua", "el salvador", "costa rica", "panama", "puerto rico", "argentina",
        "chile", "uruguay", "paraguay", "bolivia", "brazil", "french guiana", "guyana", "trinidad",
        "bahamas", "suriname", "belize", "haiti", "jamaica", "cuba"
    ]):
        return "Central & South America"
    elif any(c in country for c in [
        "saudi arabia", "united arab emirates", "kuwait", "qatar", "bahrain", "oman", "iraq",
        "syria", "jordan", "lebanon", "israel", "palestine", "egypt", "libya", "algeria", "tunisia",
        "morocco", "yemen"
    ]):
        return "Middle East & North Africa"
    elif any(c in country for c in [
        "nigeria", "kenya", "ghana", "south africa", "ethiopia", "tanzania", "uganda", "zambia",
        "zimbabwe", "namibia", "botswana", "lesotho", "eswatini", "mozambique", "angola", "cameroon",
        "senegal", "ivory coast", "sudan", "south sudan", "rwanda", "burundi", "somalia", "chad",
        "democratic republic of the congo", "republic of the congo", "gabon", "guinea", "guinea-bissau",
        "togo", "benin", "central african republic", "mali", "burkina faso", "liberia", "sierra leone",
        "gambia", "niger"
    ]):
        return "Sub-Saharan Africa"
    elif any(c in country for c in [
        "india", "pakistan", "bangladesh", "sri lanka", "nepal", "bhutan", "maldives", "afghanistan"
    ]):
        return "South Asia"
    elif any(c in country for c in [
        "kazakhstan", "uzbekistan", "kyrgyzstan", "turkmenistan", "tajikistan", "azerbaijan", "turkey"
    ]):
        return "Central Asia"
    elif any(c in country for c in [
        "china", "taiwan", "japan", "south korea", "north korea", "mongolia"
    ]):
        return "East Asia"
    elif any(c in country for c in [
        "thailand", "vietnam", "cambodia", "laos", "myanmar", "malaysia", "indonesia", "philippines",
        "singapore", "brunei", "east timor"
    ]):
        return "Southeast Asia"
    elif any(c in country for c in [
        "papua new guinea", "fiji", "solomon islands", "vanuatu", "samoa", "tonga", "new caledonia",
        "french polynesia"
    ]):
        return "South Pacific"
    else:
        return "Other"
