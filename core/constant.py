import difflib

# Complete list of Geoapify Places categories (https://apidocs.geoapify.com/docs/places/#categories)
GEOAPIFY_CATEGORIES = [
    # Accommodation
     "accommodation",
    "accommodation.hotel",
    "accommodation.hostel",
    "accommodation.guest_house",
    "accommodation.motel",
    "accommodation.apartment",
    "accommodation.resort",
    "accommodation.villa",
    "accommodation.capsule_hotel",
    "accommodation.lodge",
    "accommodation.chalet",
    "accommodation.camping",
    "accommodation.caravan_site",

    # Catering
    "catering",
    "catering.restaurant",
    "catering.fast_food",
    "catering.cafe",
    "catering.pub",
    "catering.bar",
    "catering.food_court",
    "catering.bistro",
    "catering.barbecue",
    "catering.ice_cream",
    "catering.bakery",
    "catering.confectionery",
    "catering.juice_bar",
    "catering.suya_spot",       # Nigerian specific
    "catering.amala_joint",     # Nigerian specific
    "catering.roastery",
    "catering.tea_house",

    # Commercial
    "commercial",
    "commercial.supermarket",
    "commercial.bank",
    "commercial.atm",
    "commercial.mall",
    "commercial.department_store",
    "commercial.convenience",
    "commercial.kiosk",
    "commercial.pharmacy",
    "commercial.chemist",       # Common in Nigeria
    "commercial.optometrist",
    "commercial.market",        # For open markets
    "commercial.furniture",
    "commercial.electronics",
    "commercial.hardware",
    "commercial.clothing",
    "commercial.tailor",        # Popular in Nigeria
    "commercial.beauty_salon",
    "commercial.barber_shop",
    "commercial.laundry",
    "commercial.print_shop",
    "commercial.mobile_phone",
    "commercial.computer",
    "commercial.pawn_shop",
    "commercial.petrol_station",  # Essential for Nigeria
    "commercial.car_dealer",

    # Entertainment
    "entertainment",
    "entertainment.cinema",
    "entertainment.nightclub",
    "entertainment.theatre",
    "entertainment.casino",
    "entertainment.amusement_arcade",
    "entertainment.bowling_alley",
    "entertainment.karaoke",
    "entertainment.comedy_club",
    "entertainment.escape_game",
    "entertainment.billiards",
    "entertainment.gaming_cafe",
    "entertainment.event_venue",
    "entertainment.beer_parlour",  # Nigerian nightlife
    "entertainment.viewpoint",

    # Healthcare
    "healthcare",
    "healthcare.hospital",
    "healthcare.pharmacy",
    "healthcare.clinic",
    "healthcare.dentist",
    "healthcare.doctors",
    "healthcare.veterinary",
    "healthcare.physiotherapist",
    "healthcare.laboratory",
    "healthcare.maternity_clinic",
    "healthcare.optical",
    "healthcare.psychologist",
    "healthcare.traditional",    # For traditional medicine
    "healthcare.midwife",

    # Leisure
    "leisure",
    "leisure.park",
    "leisure.sports_centre",
    "leisure.swimming_pool",
    "leisure.golf_course",
    "leisure.stadium",

    # Religion
    "religion",
    "religion.place_of_worship",
    "religion.church",
    "religion.mosque",
    "religion.temple",
    "religion.synagogue",
    "religion.shrine",
    "religion.monastery",
    "religion.cemetery",
    "religion.graveyard",

    # Transportation
     "transportation",
    "transportation.airport",
    "transportation.bus_station",
    "transportation.car_rental",
    "transportation.parking",
    "transportation.taxi",
    "transportation.bicycle_rental",
    "transportation.motorcycle_rental",
    "transportation.ferry_terminal",
    "transportation.traffic_light",
    "transportation.charging_station",
    "transportation.bus_stop",
    "transportation.tricycle_stand",

    # Education
    "education",
    "education.school",
    "education.university",
    "education.library",
    "education.college",
    "education.kindergarten",
    "education.driving_school",
    "education.music_school",
    "education.language_school",
    "education.tutoring_center",
    "education.computer_training",
    "education.vocational_training",

    # Other
    "tourism",
    "tourism.attraction",
    "tourism.museum",
    "tourism.zoo",
    "tourism.aquarium",
    "tourism.gallery",
    "tourism.theme_park",
    "tourism.historic_site",
    "tourism.monument",
    "tourism.cultural_center",
    "tourism.beach",
    "tourism.waterfall",
    "tourism.nature_reserve",

    # Government
    "government",
    "government.police",
    "government.post_office",
    "government.fire_station",
    "government.courthouse",
    "government.embassy",
    "government.military",
    "government.prison",
    "government.townhall",
    "government.customs",
    "government.immigration",
    "government.passport_office",
    "government.driving_license_office",

    # Services
    "service",
    "service.vehicle",
    "service.vehicle.car_wash",
    "service.vehicle.repair",
    "service.vehicle.parts",
    "service.vehicle.inspection",
    "service.electrician",
    "service.plumber",
    "service.locksmith",
    "service.cleaning",
    "service.pest_control",
    "service.security",
    "service.fumigator",
    "service.generator_repair",
    "service.photographer",
    "service.funeral_services",
    "service.marriage_registry",

    # Inustrial
    "industrial",
    "industrial.factory",
    "industrial.warehouse",
    "industrial.construction",
    "industrial.farm",
    "industrial.quarry",
    "industrial.energy",

    # Nigerian specific services
    "commercial.petty_trader",   # For roadside vendors
    "catering.buka",             # Local eateries
    "catering.pepper_soup_joint",
    "commercial.cold_room",      # For frozen goods
    "service.cyber_cafe",        # Still relevant
    "service.pvc_fabrication",   # For ID cards
    "service.photocopy",
]


def match_category(user_input) -> str:
    """
    Fuzzy-matches user input to the closest Geoapify category.

    Args:
        user_input (str): User's search term (e.g., "pharmacy", "hotel")

    Returns:
        str: Matched Geoapify category (e.g., "healthcare.pharmacy") or None if no match.
    """
    user_input = user_input.lower().strip()
    matches = difflib.get_close_matches(user_input, GEOAPIFY_CATEGORIES, n=1, cutoff=0.4)
    return matches[0] if matches else None


# Example usage:
if __name__ == "__main__":
    print(match_category("chemist"))  # healthcare.pharmacy
    print(match_category("buka"))  # catering.buka (Nigerian)
    print(match_category("generator repair"))  # service.generator_repair
    print(match_category("keke stand"))