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
        except Exception as e:
            logger.error(e)

    with open('{}.jsonld'.format(jsonld_filename.split('.json')[0]), 'w', encoding='utf-8') as output_file:
        json.dump(schema_org_metadata, output_file, indent=4)


#"required" : [ "title", "types", "creators", "licenses", "description", "keywords", "version" ]
# do we only provide google jsonld for the main dataset? not hasPart datasets?
def generate_schema_org_metadata(json_obj):
    """
    The funciton to convert valid DATS json to schema.org jsol-ld
    :param json_obj: valid DATS json
    :return: jsol-ld snippet that should be embedded in html page for each individual dataset
    Test the final snipper here https://search.google.com/test/rich-results
    Example where it should go in the html:

     <body><html>
      <head>
        <title>NCDC Storm Events Database</title>
        <script type="application/ld+json">
            HERE
        </script>
      </head>
      <body>
      </body>
    </html>
    """

    schema_jsonld = {}
    schema_jsonld["@context"] = "https://schema.org/"
    schema_jsonld["@type"] = "Dataset"
    try:
        schema_jsonld["name"] = json_obj["title"]
        schema_jsonld["description"] = json_obj["description"]
        licenses = []
        for license in json_obj["licenses"]:
            licenses.append(license["name"])
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
                name = ''
                if "firstName" in creator:
                    person["givenName"] = creator["firstName"]
                    name += creator["firstName"]
                if "lastName" in creator:
                    person["familyName"] = creator["lastName"]
                    name += creator["lastName"]
                if "email" in creator:
                    person["email"] = creator["email"]
                if "fullName" in creator:
                    person["name"] = creator["fullName"]
                # schema requires 'name' or 'url' to be present for Person
                # dats doesn't have required fields for Person
                else:
                    person["name"] = "Name is not provided"
                creators.append(person)
        schema_jsonld["creator"] = creators
    except KeyError as e:
        logger.error(e)

    return schema_jsonld


def help():
    return logger.info('Usage: python schema_org_metadata.py --file=DATS.json')


if __name__ == "__main__":
    main(argv[1:])
