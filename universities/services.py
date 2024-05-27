from api_base import services

from .models import University


class UniversityServices(services.ServiceProvider):
    """
    Service provider class for Universities. This
    class provides methods to work with universities in db
    """

    def __init__(self):
        super().__init__()
        self.model = University
        self.fields = {
            "short_name": str,
            "full_name": str,
            "city": str,
            "region": str,
        }

    def get_by(self, **kwargs: dict) -> University or None:
        """
        This method is used to get a university from database by any of its fields.
        Parameters
        ----------
        kwargs : dict
            fields and their values to match
        Returns
        ----------
        University or None
            Returns University object if there is matching university, else None
        """
        if University.objects.filter(**kwargs).exists():
            return University.objects.get(**kwargs)
        return None
