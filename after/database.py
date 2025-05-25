class Database:
    def __init__(self):
        self._cities_by_county: dict[str, tuple[str, ...]] = {
            "France": ("Paris", "Lyon", "Marseille"),
            "USA": ("New York", "Los Angeles", "Chicago"),
            "Japan": ("Tokyo", "Kyoto", "Osaka"),
        }

    def get_countries(self) -> list[str]:
        return list(self._cities_by_county.keys())

    def get_cities(self, country: str) -> tuple[str, ...]:
        return self._cities_by_county[country]
