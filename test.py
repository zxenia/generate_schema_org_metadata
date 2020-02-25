import unittest
from .schema_org_metadata import generate_schema_org_metadata

EXAMPLE = {
    "title": "Test Dataset",
    "description": "Test dataset description. ",
    "dates": [
        {
            "date": "2020-01-22 00:00:00",
            "type": {
                "value": "DATS file creation date"
            }
        }
    ],
    "creators": [
        {
            "name": "Test University"
        },
        {
            "firstName": "John",
            "lastName": "Doe",
            "email": "test@example.org",
            "affiliations": [
                {"name": "University"}
            ]
        }
    ],
    "types": [
        {
            "information": {
                "value": "test"
            }
        }
    ],
    "privacy": "Open Access",
    "version": "1.0",
    "licenses": [
        {
            "name": "https://creativecommons.org/licenses/by/4.0/"
        }
    ],
    "keywords": [
    {
      "value": "test"
    },
    {
      "value": "dataset"
    }
  ]
}


# invalid dats doesn't have required 'keywords'
EXAMPLE_INVALID = {
    "title": "Test Dataset",
    "description": "Test dataset description. ",
    "dates": [
        {
            "date": "2020-01-22 00:00:00",
            "type": {
                "value": "DATS file creation date"
            }
        }
    ],
    "creators": [
        {
            "name": "Test University"
        },
        {
            "firstName": "John",
            "lastName": "Doe",
            "email": "test@example.org",
            "affiliations": [
                {"name": "University"}
            ]
        }
    ],
    "types": [
        {
            "information": {
                "value": "test"
            }
        }
    ],
    "privacy": "Open Access",
    "version": "1.0",
    "licenses": [
        {
            "name": "https://creativecommons.org/licenses/by/4.0/"
        }
    ]
}


class SchemaOrgMetadataTestCase(unittest.TestCase):
    def test_generate_schema_org_metadata(self):
        schema_org_metadata = generate_schema_org_metadata(EXAMPLE)
        self.assertEqual(schema_org_metadata["@context"], 'https://schema.org/')

    def test_invalid_example(self):
        generate_schema_org_metadata(EXAMPLE_INVALID)
        self.assertRaises(KeyError)


if __name__ == '__main__':
    unittest.main()
