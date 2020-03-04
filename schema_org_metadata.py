import json
import logging
import getopt
from sys import argv


logger = logging.getLogger(__name__)

def main(argv):
    FORMAT = '%(message)s'
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.INFO)
    opts, args = getopt.getopt(argv, "", ["file=",])
    jsonld_filename = ''

    for opt, arg in opts:
        if opt == '--file':
            jsonld_filename = arg

    if jsonld_filename == '':
        help()
        exit()

    with open(jsonld_filename) as json_file:
        json_obj = json.load(json_file)
        try:
            schema_org_metadata = generate_schema_org_metadata(json_obj)
            if schema_org_metadata:
                with open('{}.jsonld'.format(jsonld_filename.split('.json')[0]), 'w', encoding='utf-8') as output_file:
                    json.dump(schema_org_metadata, output_file, indent=4)
        except Exception as e:
            logger.error(e)


def generate_schema_org_metadata(json_obj):
    """
    The function to convert valid DATS json to schema.org json-ld.
    DATS required fields: [ "title", "types", "creators", "licenses", "description", "keywords", "version" ]

    :param json_obj: valid DATS json
    :return: jsol-ld snippet that should be embedded in html page for each individual dataset
    Test the final snippet here https://search.google.com/test/rich-results

    Example where json-ld should go in the html:

     <body><html>
      <head>
        <title>Database title</title>
        <script type="application/ld+json">
            HERE
        </script>
      </head>
      <body>
      </body>
    </html>
    """
    try:
        schema_jsonld = {}
        schema_jsonld["@context"] = "https://schema.org/"
        schema_jsonld["@type"] = "Dataset"
        # required fields
        schema_jsonld["name"] = json_obj["title"]
        schema_jsonld["description"] = json_obj["description"]
        schema_jsonld["version"] = json_obj["version"]
        licenses = []
        for license in json_obj["licenses"]:
            # license can be of type URL or CreativeWork
            if license["name"].startswith("http"):
                licenses.append(license["name"])
            else:
                license_creative_work = {}
                license_creative_work["@type"] = "CreativeWork"
                license_creative_work["name"] = license["name"]
                licenses.append(license_creative_work)
        schema_jsonld["license"] = licenses
        keywords = []
        for keyword in json_obj["keywords"]:
            keywords.append(keyword["value"])
        schema_jsonld["keywords"] = keywords
        creators = []
        for creator in json_obj["creators"]:
            if "name" in creator:
                organization = {}
                organization["@type"] = "Organization"
                organization["name"] = creator["name"]
                creators.append(organization)
            else:
                person = {}
                person["@type"] = "Person"
                # all fields below are not required so we have to check if they are present
                if "firstName" in creator:
                    person["givenName"] = creator["firstName"]
                if "lastName" in creator:
                    person["familyName"] = creator["lastName"]
                if "email" in creator:
                    person["email"] = creator["email"]
                # schema.org requires 'name' or 'url' to be present for Person
                # dats doesn't have required fields for Person,
                # therefore in case when no 'fullName' provided or one of 'firstName' or 'lastName' is not provided
                # we set a placeholder for 'name'
                if "fullName" in creator:
                    person["name"] = creator["fullName"]
                elif all (k in creator for k in ("firstName", "lastName")):
                    person["name"] = creator["firstName"] + " " + creator["lastName"]
                else:
                    person["name"] = "Name is not provided"
                # check for person affiliations
                if "affiliations" in creator:
                    affiliation = []
                    for affiliated_org in creator["affiliations"]:
                        organization = {}
                        organization["@type"] = "Organization"
                        organization["name"] = affiliated_org["name"]
                        affiliation.append(organization)
                    person["affiliation"] = affiliation
                creators.append(person)
        schema_jsonld["creator"] = creators
        return schema_jsonld

    except KeyError as e:
        logger.error(e)
        return None


def help():
    return logger.info('Usage: python schema_org_metadata.py --file=DATS.json')


if __name__ == "__main__":
    main(argv[1:])
