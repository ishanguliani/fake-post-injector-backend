from django.db import models

class Configuration(models.Model):
    CHOICES = [
            ('0', '0(never clone)'),
            ('1', '1'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
            ('10', '10(always clone)'),
            ]
    chances_of_cloning = models.CharField(max_length=2, default='5', choices=CHOICES, blank=True)
    should_show_red_banner_for_injected_posts = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return "chances of cloning: " + str(self.chances_of_cloning) + ", show red banner: " + str(self.should_show_red_banner_for_injected_posts)
