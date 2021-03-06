# adiscorduser.com

Source code for [adiscorduser.com](https://www.adiscorduser.com).

## Getting started

1. To begin, you will need to [create a virtual environment](https://docs.python.org/3/tutorial/venv.html) and then activate it.

2. Once you have activated your virtual environment, you can install the required packages. Run `pip install -r requirements.txt` in your shell.

3. After that, you must rename the settings files [mock_dev.py](adiscorduser/settings/mock_dev.py) and [mock_prod.py](adiscorduser/settings/mock_prod.py) to `dev.py` and `prod.py`.

4. Open both of the settings files and change the database credentials to fit your setup. Change `ALLOWED_HOSTS` to your domain (or `localhost`) and change `SECRET_KEY` to a secret key.

5. Change `MEDIA_ROOT` to the directory where you would like media for the uploader to be stored. Afterwards, in the `MEDIA` dictionary, set `MEDIA["image"]["url"]` and `MEDIA["video"]["url"]` to the base URLs that should be returned after media is created. There should be a trailing slash at the end of the base URLs.

6. If you are using Cloudflare, you will need to change `CLOUDFLARE["ZONE_IDENTIFIER"]` and `CLOUDFLARE["API_KEY"]` to your zone identifier and API key. Otherwise, remove the `CLOUDFLARE` dictionary.

7. Now, you will need to create migrations for the database. Run `python manage.py migrate` in your shell. This should create all of the necessary tables in your database for running the site.

You're done! You should now have everything configured to run the site in production or using Django's development server.

### Starting a development instance

1. Set `DJANGO_SETTINGS_MODULE` environment variable to the location of the settings file you are using. For example, if you're using the development settings file, you should set the variable to `adiscorduser.settings.dev`.

2. Run `python manage.py runserver` in your shell. This will start a development instance of the site.

### Running in production

**Note:** I recommend using uWSGI for running the site in production. You can use other methods, but the one documented here is for uWSGI.

1. Run `pip install uwsgi` to install uWSGI.

2. Edit the [configuration file](adiscorduser/uwsgi.ini). The default configuration file is suited for my environment, but yours will likely vary.

3. To verify that the site runs successfully, I highly recommend starting up an instance of uWSGI from your shell to make sure that the site is served correctly. Run `uwsgi /path/to/uwsgi.ini` (with `/path/to/uwsgi.ini` replaced with the path to the configuration file mentioned in the above step) and then, if you have the configuration file set the serve the site on an HTTP socket, open it in your web browser.

4. If that works, you should be good to go. You will probably want to either put the site behind a reverse proxy, or run the above command as a service. You can learn more about doing that on [uWSGI's site](https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html).

## Development

For the main website (in the `core` app), the code is basic, undocumented, and lacks tests. The planned redesign is supposed to fix these problems and also introduce documentation for the `uploader` app.

### Running tests

1. In your media directory (specified in `MEDIA_ROOT`), create a subdirectory called `examples`.

2. Populate `examples` with images and videos to be used for tests. The naming scheme should be `<media file extension>.<media file extension>` (eg. `mp4.mp4` or `png.png`). Do this for all of the media types in the `MEDIA` dictionary in your settings.

3. Run `python manage.py test` in your shell.

**Note:** Test coverage in the `uploader` app isn't adequate, and the `core` app lacks tests entirely.

## Licensing

This project is licensed under the [MIT License](LICENSE.txt). Any evidence of license violations should be directed to copyright@adiscorduser.com.

---
Made with ❤️ by A Discord User#1173.