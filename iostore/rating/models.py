from django.db import models
from users.models import User

class Rating(models.Model):
    """
    Dividing the items by categories to allow filtering

    Attributes
    ----------
    yay
        users voted yay for category
    nay
        users voted nay for category
    sumy
        sum of `yays` users ratings
    sumn
        sum of `nays` users ratings

    Notes
    -----
    * sums should be maintained on user rating change, example:
        sumy = sumy - old_user_rating + new_user_rating
    * validity rating for each category would be `sumy` / `sumn`
    """
    yays = models.ManyToManyField(User, related_name='yays')
    nays = models.ManyToManyField(User, related_name='nays')
    sumy = models.FloatField()
    sumn = models.FloatField()

    def __str__(self):
        return self.name