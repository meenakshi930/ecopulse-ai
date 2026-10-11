import requests


def get_species_info(species_name):

    url = "https://api.inaturalist.org/v1/taxa"

    params = {
        "q": species_name,
        "rank": "species",
        "per_page": 5
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            return None

        taxon = results[0]

        return {
            "name": taxon.get("name"),
            "common_name": taxon.get("preferred_common_name"),
            "rank": taxon.get("rank"),
            "wikipedia_url": taxon.get("wikipedia_url"),
            "observations_count": taxon.get("observations_count")
        }

    except requests.RequestException as e:

        print(f"iNaturalist request failed: {e}")

        return None