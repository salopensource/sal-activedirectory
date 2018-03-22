# Django settings for sal project.
from system_settings import *
from settings_import import *

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': os.path.join(PROJECT_DIR, 'db/sal.db'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Memcached
if 'MEMCACHED_PORT_11211_TCP_ADDR' in os.environ:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [
                '%s:%s' % (os.environ['MEMCACHED_PORT_11211_TCP_ADDR'],
                           os.environ['MEMCACHED_PORT_11211_TCP_PORT']),
            ]
        }
    }

# PG Database
host = None
port = None

if 'DB_USER' in os.environ:
    if 'DB_HOST' in os.environ:
        host = os.environ.get('DB_HOST')
        port = os.environ.get('DB_PORT', '5432')

    elif 'DB_PORT_5432_TCP_ADDR' in os.environ:
        host = os.environ.get('DB_PORT_5432_TCP_ADDR')
        port = os.environ.get('DB_PORT_5432_TCP_PORT', '5432')

    else:
        host = 'db'
        port = '5432'

if host and port:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'HOST': host,
            'PORT': port,
        }
    }

# ActiveDirectory Connection
AUTHENTICATION_BACKENDS = [
    'server.ADAuthentication.ADAuthentication',
    'django.contrib.auth.backends.ModelBackend',
]
AUTH_LDAP_SERVER_URI = 'ldaps://hostname.company.com:636'
AUTH_LDAP_USER_DOMAIN = 'company.com'
AUTH_LDAP_USER_SEARCH = ('DC=ch,DC=ads,DC=company,DC=com',
                         'DC=uk,DC=ads,DC=company,DC=com',
                         'DC=us,DC=ads,DC=company,DC=com')
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "sAMAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}
AUTH_LDAP_USER_PREFIX = 'ldap_' # Prefix of django username compared to ldap username

# LDAP SAL Mapping
AUTH_LDAP_USER_PROFILE = {
                            'RO': ('CN=users-all,DC=department,DC=ad,DC=company,DC=com',),
                            'RW': ('CN=service-desk,DC=department,DC=ad,DC=company,DC=com',
                                   'CN=group-leader,OU=group,DC=department,DC=ad,DC=company,DC=com'),
                            'GA': 'CN=admin,DC=department,DC=ad,DC=company,DC=com',
                        }

AUTH_LDAP_USER_TO_BUSINESS_UNIT = {
                            '#ALL_BU': ('CN=service-desk,OU=it,DC=ad,DC=company,DC=com',
                                        'CN=sysadmins,OU=it,DC=ad,DC=company,DC=com',),
                            'CH':      ('CN=mac-admins,OU=it,DC=ch,DC=ad,DC=company,DC=com',),
                            'UK':      ('CN=mac-admins,OU=it,DC=uk,DC=ad,DC=company,DC=com',),
                            'US':       'CN=mac-admins,OU=it,DC=us,DC=ad,DC=company,DC=com',
                        }
