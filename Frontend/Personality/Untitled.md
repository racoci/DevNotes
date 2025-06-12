I discovered more queries from the Personality Database API that we can use on our system:

## Suggestions
Doing something like this I can get suggestions
```js
fetch("https://api.personality-database.com/api/v2/search/suggestion?query=Gon", {
  "headers": {
    "accept": "*/*",
    "accept-language": "pt,en-US;q=0.9,en;q=0.8,es-MX;q=0.7,es;q=0.6,pt-BR;q=0.5",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "cookie": "_cc_id=b3891131335dd45c069588379984a74d; __qca=P1-3a947a83-80e4-4450-8803-388661ea13b0; panoramaId_expiry=1750032286292; panoramaId=869e0edee14bf7cd02fbb8b11c7c185ca02cd32827dfa029e4babccb02329436; cto_bundle=cV_kYl9XQ3ZvYmZZY3ZEYWQlMkZqdFRUc2oyOXNCcXg3eU9QM1NhcFZPJTJGS3RNTTlFJTJGMTJ6MTRsRjg3aFZUcEpXZDJiYWEwWlElMkIlMkJmOHVGMjdJRG5JSVJrQVRWcDNXQWdBT3E3RktOZ1drVERXWWlCU2FJZzFSdEY1eEtvQTdNJTJCU0NDNU9KendhZ3d1QkVYVjNneDlkWUk3T3E3VnRRY1pLdFN2QXNlVndQb1NKZUFEUFZXUkdWdkNyZ1BKMDdHMHlUMGhYeVk3R3JoQVozOVNCdnlLMUlLa1ZCRWZ6QWdYa2U1ZlQzMUtQa0tlVyUyRjk4em5KeGo0ZGhQd2VzQ2lDT0hPTEpNY2xXWDRmOEFoTGdVT3hLc0FmUzlzdiUyRlElM0QlM0Q; X-Lang=en-US; X-TZ-Database-Name=America/Sao_Paulo; _ga=GA1.2.499971693.1747080796; _gid=GA1.2.2113425451.1749749883; __gads=ID=f5d6fcb935d02934:T=1747080798:RT=1749749884:S=ALNI_MbEzTnytdEc_WVuzxHQSFaZkKy_ZQ; __eoi=ID=ed8cdbc75dd84050:T=1747080798:RT=1749749884:S=AA-Afja36jS34gul40Z5mE6Ql6En; FCNEC=%5B%5B%22AKsRol991BcXCpdipkDteDDqcx4Z4ANgsp6sAzMa1yDZxr2f-mKr4Y4qhu9l35q2vyBJZ9emnkbojnTpxktGVM4xdHGNUkCd2_xjpQ_6n8ZFODZpjJX-qExAeZ_4_vMgbYbwFoKuqFUHi1svPBaYORj9DFhmG7WQ0g%3D%3D%22%5D%5D; _ga_8S3H6J5GSR=GS2.1.s1749749882$o15$g1$t1749750140$j38$l0$h0",
    "Referer": "https://www.personality-database.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": null,
  "method": "GET"
});
```

Example response:

```json
{
    "data": {
        "count": 12,
        "cursor": {
            "limit": 0,
            "nextCursor": ""
        },
        "results": [
            {
                "type": "subcategory",
                "subcategory": {
                    "type": "subcategory",
                    "id": "49061",
                    "name": "Gon (ゴン?)",
                    "altName": "",
                    "group": "",
                    "image": {
                        "picURL": "https://static1.personalitydatabase.net/2/pdb-subcat-images-prod/55799f94/subcategory_images/6ea7241531c64606b7688ff01b5519e5.png"
                    },
                    "catIcon": {
                        "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                    },
                    "topProfiles": "",
                    "profileCount": 1,
                    "i18n": {
                        "detectedLanguage": "en",
                        "en": "Gon (ゴン?)"
                    },
                    "propertyID": "2",
                    "categoryID": "8",
                    "isFictional": true
                }
            },
            {
                "type": "subcategory",
                "subcategory": {
                    "type": "subcategory",
                    "id": "24891",
                    "name": "Let's La Gon",
                    "altName": "",
                    "group": "Comedy",
                    "image": {
                        "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/2bca34cd/profile_images/af286fb16d6e48abac8f17f69c8947ba.png"
                    },
                    "catIcon": {
                        "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                    },
                    "topProfiles": "",
                    "profileCount": 2,
                    "i18n": {
                        "detectedLanguage": "en",
                        "en": "Let's La Gon"
                    },
                    "propertyID": "2",
                    "categoryID": "8",
                    "isFictional": true
                }
            },
            {
                "type": "profile",
                "profile": {
                    "subcatID": "190",
                    "subcategory": "Hunter X Hunter",
                    "id": "2126",
                    "name": "Gon Freecss",
                    "image": {
                        "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/f3ddfa26/profile_images/02779f99c78745ceb5f3216b666328aa.png"
                    },
                    "catIcon": {
                        "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                    },
                    "subcategories": [
                        {
                            "id": "190",
                            "name": "Hunter X Hunter",
                            "image": null,
                            "catIcon": null
                        }
                    ],
                    "personalities": [
                        {
                            "system": "Four Letter",
                            "personality": "ESFP"
                        },
                        {
                            "system": "Enneagram",
                            "personality": "8w7"
                        }
                    ],
                    "allowVoting": true,
                    "visibility": "Full",
                    "i18n": {
                        "detectedLanguage": "en",
                        "en": "Gon Freecss"
                    },
                    "propertyID": "2",
                    "categoryID": "8",
                    "isMeme": false,
                    "isCharacter": true,
                    "isCelebrity": false,
                    "topAnalysis": {
                        "type": "analysis",
                        "id": "10513998",
                        "content": "มีความสดใสมาก ชอบให้การปฏิบัติ ทําสิ่งที่ตัวเองชอบ สดใส ร่าเริง มีความแข็งแกร่ง",
                        "functionList": null
                    },
                    "showProfileReaction": false,
                    "profileReactions": null
                }
            },
            {
                "type": "profile",
                "profile": {
                    "subcatID": "14",
                    "subcategory": "Star Wars",
                    "id": "61",
                    "name": "Qui-Gon Jinn",
                    "image": {
                        "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/7047160/profile_images/3e9e28270a72486db8705648c7703828.png"
                    },
                    "catIcon": {
                        "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/c52e1e1c/category_icon_v2/cat_3.png"
                    },
                    "subcategories": [
                        {
                            "id": "14",
                            "name": "Star Wars",
                            "image": null,
                            "catIcon": null
                        }
                    ],
                    "personalities": [
                        {
                            "system": "Four Letter",
                            "personality": "INFJ"
                        },
                        {
                            "system": "Enneagram",
                            "personality": "9w8"
                        }
                    ],
                    "allowVoting": true,
                    "visibility": "Full",
                    "i18n": {
                        "detectedLanguage": "en",
                        "en": "Qui-Gon Jinn"
                    },
                    "propertyID": "2",
                    "categoryID": "3",
                    "isMeme": false,
                    "isCharacter": true,
                    "isCelebrity": false,
                    "topAnalysis": {
                        "type": "analysis",
                        "id": "5693090",
                        "content": "”I don't sense anything.",
                        "functionList": null
                    },
                    "showProfileReaction": false,
                    "profileReactions": null
                }
            },
            {
                "type": "text",
                "text": "Lee Gon"
            },
            {
                "type": "text",
                "text": "Gon Freecss"
            },
            {
                "type": "text",
                "text": "I didn't get no sleep cause of y'all, you're not gon' get no sleep cause of me"
            },
            {
                "type": "text",
                "text": "Yoo-Gon"
            },
            {
                "type": "text",
                "text": "Gon (Yun Leesu)"
            },
            {
                "type": "text",
                "text": "Ta Gon"
            },
            {
                "type": "text",
                "text": "Gon"
            },
            {
                "type": "text",
                "text": "Young-Gon O"
            }
        ]
    },
    "error": {
        "code": "S20000",
        "message": "OK",
        "details": {}
    }
}
```

## Top

```js
fetch("https://api.personality-database.com/api/v2/search/top?query=Gon&limit=20&nextCursor=0", {
  "headers": {
    "accept": "*/*",
    "accept-language": "pt,en-US;q=0.9,en;q=0.8,es-MX;q=0.7,es;q=0.6,pt-BR;q=0.5",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "cookie": "_cc_id=b3891131335dd45c069588379984a74d; __qca=P1-3a947a83-80e4-4450-8803-388661ea13b0; panoramaId_expiry=1750032286292; panoramaId=869e0edee14bf7cd02fbb8b11c7c185ca02cd32827dfa029e4babccb02329436; cto_bundle=cV_kYl9XQ3ZvYmZZY3ZEYWQlMkZqdFRUc2oyOXNCcXg3eU9QM1NhcFZPJTJGS3RNTTlFJTJGMTJ6MTRsRjg3aFZUcEpXZDJiYWEwWlElMkIlMkJmOHVGMjdJRG5JSVJrQVRWcDNXQWdBT3E3RktOZ1drVERXWWlCU2FJZzFSdEY1eEtvQTdNJTJCU0NDNU9KendhZ3d1QkVYVjNneDlkWUk3T3E3VnRRY1pLdFN2QXNlVndQb1NKZUFEUFZXUkdWdkNyZ1BKMDdHMHlUMGhYeVk3R3JoQVozOVNCdnlLMUlLa1ZCRWZ6QWdYa2U1ZlQzMUtQa0tlVyUyRjk4em5KeGo0ZGhQd2VzQ2lDT0hPTEpNY2xXWDRmOEFoTGdVT3hLc0FmUzlzdiUyRlElM0QlM0Q; X-Lang=en-US; X-TZ-Database-Name=America/Sao_Paulo; _ga=GA1.2.499971693.1747080796; _gid=GA1.2.2113425451.1749749883; __gads=ID=f5d6fcb935d02934:T=1747080798:RT=1749749884:S=ALNI_MbEzTnytdEc_WVuzxHQSFaZkKy_ZQ; __eoi=ID=ed8cdbc75dd84050:T=1747080798:RT=1749749884:S=AA-Afja36jS34gul40Z5mE6Ql6En; FCNEC=%5B%5B%22AKsRol991BcXCpdipkDteDDqcx4Z4ANgsp6sAzMa1yDZxr2f-mKr4Y4qhu9l35q2vyBJZ9emnkbojnTpxktGVM4xdHGNUkCd2_xjpQ_6n8ZFODZpjJX-qExAeZ_4_vMgbYbwFoKuqFUHi1svPBaYORj9DFhmG7WQ0g%3D%3D%22%5D%5D; _ga_8S3H6J5GSR=GS2.1.s1749749882$o15$g1$t1749750140$j38$l0$h0",
    "Referer": "https://www.personality-database.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": null,
  "method": "GET"
});
```

Returns something like this:

```json
{
    "data": {
        "profiles": [
            {
                "subcatID": "190",
                "subcategory": "Hunter X Hunter",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Hunter X Hunter"
                },
                "id": "2126",
                "name": "Gon Freecss",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/f3ddfa26/profile_images/02779f99c78745ceb5f3216b666328aa.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                },
                "subcategories": [
                    {
                        "id": "190",
                        "name": "Hunter X Hunter",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Hunter X Hunter"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ESFP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "8w7"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Gon Freecss"
                },
                "propertyID": "2",
                "categoryID": "8",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=2126",
                "topAnalysis": {
                    "type": "analysis",
                    "id": "10513998",
                    "content": "มีความสดใสมาก ชอบให้การปฏิบัติ ทําสิ่งที่ตัวเองชอบ สดใส ร่าเริง มีความแข็งแกร่ง",
                    "functionList": null
                },
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "14",
                "subcategory": "Star Wars",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Star Wars"
                },
                "id": "61",
                "name": "Qui-Gon Jinn",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/7047160/profile_images/3e9e28270a72486db8705648c7703828.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/c52e1e1c/category_icon_v2/cat_3.png"
                },
                "subcategories": [
                    {
                        "id": "14",
                        "name": "Star Wars",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Star Wars"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "INFJ"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "9w8"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Qui-Gon Jinn"
                },
                "propertyID": "2",
                "categoryID": "3",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=61",
                "topAnalysis": {
                    "type": "analysis",
                    "id": "5693090",
                    "content": "”I don't sense anything.",
                    "functionList": null
                },
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "8652",
                "subcategory": "The King: Eternal  Monarch",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "The King: Eternal  Monarch"
                },
                "id": "122462",
                "name": "Lee Gon",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/53644005/profile_images/306b09b1010e4bb297d4d695e0b8bf61.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/f84e37ac/category_icon_v2/cat_2.png"
                },
                "subcategories": [
                    {
                        "id": "8652",
                        "name": "The King: Eternal  Monarch",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "The King: Eternal  Monarch"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "INFJ"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "5w4"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Lee Gon"
                },
                "propertyID": "2",
                "categoryID": "2",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=122462",
                "topAnalysis": {
                    "type": "analysis",
                    "id": "944651",
                    "content": "Ni because he is effective at handling paradoxical evidence due to linear mindset, has Se that's why takes the risk of going into another dimension to find the girl he thought has saved his life, Fe because he cares about the kingdom more from his ownself, which a risk might cause him to sacrifice the love he longed to find, Ti because has the most random information 😅 apart from liking the subjects he likes.",
                    "functionList": null
                },
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "7312",
                "subcategory": "Hunter X Hunter (1999)",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Hunter X Hunter (1999)"
                },
                "id": "119714",
                "name": "Gon Freecss",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/31d1250d/profile_images/9e9a40c2bc9d4ca0b4c1f66d9845fdd1.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                },
                "subcategories": [
                    {
                        "id": "7312",
                        "name": "Hunter X Hunter (1999)",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Hunter X Hunter (1999)"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ESFP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "8w7"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Gon Freecss"
                },
                "propertyID": "2",
                "categoryID": "8",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=119714",
                "topAnalysis": {
                    "type": "analysis",
                    "id": "4926292",
                    "content": "well he is an 8 on this page at least",
                    "functionList": null
                },
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "3471",
                "subcategory": "Memes Online",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Memes Online"
                },
                "id": "60315",
                "name": "I didn't get no sleep cause of y'all, you're not gon' get no sleep cause of me",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/b3aad5ae/profile_images/2a608c79f1cb4f13a9d14e76151de06a.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/5ca85e06/category_icon_v2/cat_32.png"
                },
                "subcategories": [
                    {
                        "id": "3471",
                        "name": "Memes Online",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Memes Online"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ESTJ"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "8w7"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "I didn't get no sleep cause of y'all, you're not gon' get no sleep cause of me"
                },
                "propertyID": "3",
                "categoryID": "32",
                "isMeme": true,
                "isCharacter": false,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=60315",
                "topAnalysis": {
                    "type": "analysis",
                    "id": "59941",
                    "content": "The revenge",
                    "functionList": null
                },
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "36556",
                "subcategory": "Midnight Men ",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Midnight Men "
                },
                "id": "1132242",
                "name": "Yoo-Gon",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/463c1cd5/profile_images/dd3fa37248294af9b7f656098bf9c546.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/62742b63/category_icon_v2/cat_26.png"
                },
                "subcategories": [
                    {
                        "id": "36556",
                        "name": "Midnight Men ",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Midnight Men "
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ENFJ"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "3w2"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Yoo-Gon"
                },
                "propertyID": "2",
                "categoryID": "26",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=1132242",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "20021",
                "subcategory": "Almond (아몬드)",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Almond (아몬드)"
                },
                "id": "319514",
                "name": "Gon (Yun Leesu)",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/8b58c3a2/profile_images/9af6bc2406814732ad9a58d91f074d6f.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/1160ff0d/category_icon_v2/cat_12.png"
                },
                "subcategories": [
                    {
                        "id": "20021",
                        "name": "Almond (아몬드)",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Almond (아몬드)"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ESFP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "8w7"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Gon (Yun Leesu)"
                },
                "propertyID": "2",
                "categoryID": "12",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=319514",
                "topAnalysis": {
                    "type": "analysis",
                    "id": "4469598",
                    "content": "if someone ever reads this hellooo, i loved this book goni was my fav",
                    "functionList": null
                },
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "3865",
                "subcategory": "Arthdal Chronicles",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Arthdal Chronicles"
                },
                "id": "38281",
                "name": "Ta Gon",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/187cba81/profile_images/1356d3a7a76b44f38c1bb6dc2af96569.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/f84e37ac/category_icon_v2/cat_2.png"
                },
                "subcategories": [
                    {
                        "id": "3865",
                        "name": "Arthdal Chronicles",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Arthdal Chronicles"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ENTJ"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "3w4"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Ta Gon"
                },
                "propertyID": "2",
                "categoryID": "2",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=38281",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "3241",
                "subcategory": "Beastars",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Beastars"
                },
                "id": "285514",
                "name": "Gon",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/9b28fbbf/profile_images/98b770496e714a48a9279188a51ed359.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                },
                "subcategories": [
                    {
                        "id": "3241",
                        "name": "Beastars",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Beastars"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ENFP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "9w8"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Gon"
                },
                "propertyID": "2",
                "categoryID": "8",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=285514",
                "topAnalysis": {
                    "type": "analysis",
                    "id": "3263040",
                    "content": "Seems like an Fi user.",
                    "functionList": null
                },
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "5634",
                "subcategory": "Cheese in the Trap",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Cheese in the Trap"
                },
                "id": "127968",
                "name": "Young-Gon O",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/e381329b/profile_images/cd6388841c6d45d884fc8faa4d00272c.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/62742b63/category_icon_v2/cat_26.png"
                },
                "subcategories": [
                    {
                        "id": "5634",
                        "name": "Cheese in the Trap",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Cheese in the Trap"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ESFP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "7w8"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Young-Gon O"
                },
                "propertyID": "2",
                "categoryID": "26",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=127968",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "5617",
                "subcategory": "2000's Songs",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "2000's Songs"
                },
                "id": "160017",
                "name": "DMX - X Gon' Give It to Ya",
                "image": null,
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/61c877b6/category_icon_v2/cat_33.png"
                },
                "subcategories": [
                    {
                        "id": "5617",
                        "name": "2000's Songs",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "2000's Songs"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ESTP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "8w7"
                    }
                ],
                "allowVoting": true,
                "propertyID": "3",
                "categoryID": "33",
                "isMeme": true,
                "isCharacter": false,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=160017",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "479",
                "subcategory": "Tekken",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Tekken"
                },
                "id": "81387",
                "name": "Gon",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/b283a293/profile_images/e66726f4e30d4178b6b57009b524d348.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/56c085dd/category_icon_v2/cat_11.png"
                },
                "subcategories": [
                    {
                        "id": "479",
                        "name": "Tekken",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Tekken"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": ""
                    },
                    {
                        "system": "Enneagram",
                        "personality": "7w8"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Gon"
                },
                "propertyID": "2",
                "categoryID": "11",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=81387",
                "topAnalysis": {
                    "type": "analysis",
                    "id": "10476406",
                    "content": "My favorite character, Gon from Tekken.",
                    "functionList": null
                },
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "3864",
                "subcategory": "Cheese in the Trap (2016)",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Cheese in the Trap (2016)"
                },
                "id": "238370",
                "name": "Oh Young Gon",
                "image": null,
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/f84e37ac/category_icon_v2/cat_2.png"
                },
                "subcategories": [
                    {
                        "id": "3864",
                        "name": "Cheese in the Trap (2016)",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Cheese in the Trap (2016)"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "INTP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "5w4"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Oh Young Gon"
                },
                "propertyID": "2",
                "categoryID": "2",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=238370",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "27520",
                "subcategory": "Rookie Cops",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Rookie Cops"
                },
                "id": "456842",
                "name": "Cha Yu-Gon",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/834a58cf/profile_images/fa0bb2372da04de394b4419a7146b563.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/f84e37ac/category_icon_v2/cat_2.png"
                },
                "subcategories": [
                    {
                        "id": "27520",
                        "name": "Rookie Cops",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Rookie Cops"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ENFJ"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "2w3"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Cha Yu-Gon"
                },
                "propertyID": "2",
                "categoryID": "2",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=456842",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "30493",
                "subcategory": "Marine Corps Universe (Haebyeong Moonhak)",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Marine Corps Universe (Haebyeong Moonhak)"
                },
                "id": "490774",
                "name": "Cheol-Gon Park",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/a87d8690/profile_images/e706413cb1a442f9a7c061f4b4bbd880.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/1160ff0d/category_icon_v2/cat_12.png"
                },
                "subcategories": [
                    {
                        "id": "30493",
                        "name": "Marine Corps Universe (Haebyeong Moonhak)",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Marine Corps Universe (Haebyeong Moonhak)"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ENTJ"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "1w2"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Cheol-Gon Park"
                },
                "propertyID": "2",
                "categoryID": "12",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=490774",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "8006",
                "subcategory": "Love By Chance",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Love By Chance"
                },
                "id": "270533",
                "name": "GonHin",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/b8cd04c2/profile_images/bb3919bc9ae041b3b67079b5d13129d7.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/f84e37ac/category_icon_v2/cat_2.png"
                },
                "subcategories": [
                    {
                        "id": "8006",
                        "name": "Love By Chance",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Love By Chance"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ESFJ"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "1w2"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "GonHin"
                },
                "propertyID": "2",
                "categoryID": "2",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=270533",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "6614",
                "subcategory": "Uchi Tama?! Uchi no Tama Shirimasen ka?",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Uchi Tama?! Uchi no Tama Shirimasen ka?"
                },
                "id": "94330",
                "name": "Noda Gon",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/9eafa2e/profile_images/7cf36c0dac904bed8ed71348219da3b5.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                },
                "subcategories": [
                    {
                        "id": "6614",
                        "name": "Uchi Tama?! Uchi no Tama Shirimasen ka?",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Uchi Tama?! Uchi no Tama Shirimasen ka?"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "INFJ"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "9w1"
                    }
                ],
                "allowVoting": true,
                "propertyID": "2",
                "categoryID": "8",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=94330",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "12078",
                "subcategory": "Fall Guys: Ultimate Knockout",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Fall Guys: Ultimate Knockout"
                },
                "id": "186718",
                "name": "Hex-A-Gon",
                "image": null,
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/56c085dd/category_icon_v2/cat_11.png"
                },
                "subcategories": [
                    {
                        "id": "12078",
                        "name": "Fall Guys: Ultimate Knockout",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Fall Guys: Ultimate Knockout"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ESTP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "8w7"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Hex-A-Gon"
                },
                "propertyID": "2",
                "categoryID": "11",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=186718",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "2043",
                "subcategory": "Pocket Monsters SPECIAL",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Pocket Monsters SPECIAL"
                },
                "id": "99748",
                "name": "Snor/Red's Snorlax (Gon/Red's Kabigon)",
                "image": null,
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                },
                "subcategories": [
                    {
                        "id": "2043",
                        "name": "Pocket Monsters SPECIAL",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Pocket Monsters SPECIAL"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "INTP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "9w8"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Snor/Red's Snorlax (Gon/Red's Kabigon)"
                },
                "propertyID": "2",
                "categoryID": "8",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=99748",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "4121",
                "subcategory": "Vagabond",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Vagabond"
                },
                "id": "469296",
                "name": "Gon",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/25c98e3b/profile_images/22299a85c3d14687bc2b86871434b523.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                },
                "subcategories": [
                    {
                        "id": "4121",
                        "name": "Vagabond",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Vagabond"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ESFJ"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "2w1"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Gon"
                },
                "propertyID": "2",
                "categoryID": "8",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=469296",
                "showProfileReaction": false,
                "profileReactions": null
            }
        ],
        "subcategories": [
            {
                "id": "49061",
                "name": "Gon (ゴン?)",
                "altName": "",
                "group": "",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-subcat-images-prod/55799f94/subcategory_images/6ea7241531c64606b7688ff01b5519e5.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                },
                "topProfiles": "",
                "profileCount": 1,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Gon (ゴン?)"
                },
                "propertyID": "2",
                "categoryID": "8",
                "isFictional": true
            },
            {
                "id": "24891",
                "name": "Let's La Gon",
                "altName": "",
                "group": "Comedy",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/2bca34cd/profile_images/af286fb16d6e48abac8f17f69c8947ba.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                },
                "topProfiles": "",
                "profileCount": 2,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Let's La Gon"
                },
                "propertyID": "2",
                "categoryID": "8",
                "isFictional": true
            }
        ],
        "boards": [],
        "hint": null,
        "recommendProfiles": null
    },
    "error": {
        "code": "S20000",
        "message": "OK",
        "details": {}
    }
}
```

# Profiles:

```js
fetch("https://api.personality-database.com/api/v2/search/profiles?query=Android%2018&limit=20&nextCursor=0&pid=0&catID=0", {
  "headers": {
    "accept": "*/*",
    "accept-language": "pt,en-US;q=0.9,en;q=0.8,es-MX;q=0.7,es;q=0.6,pt-BR;q=0.5",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "cookie": "_cc_id=b3891131335dd45c069588379984a74d; __qca=P1-3a947a83-80e4-4450-8803-388661ea13b0; panoramaId_expiry=1750032286292; panoramaId=869e0edee14bf7cd02fbb8b11c7c185ca02cd32827dfa029e4babccb02329436; cto_bundle=cV_kYl9XQ3ZvYmZZY3ZEYWQlMkZqdFRUc2oyOXNCcXg3eU9QM1NhcFZPJTJGS3RNTTlFJTJGMTJ6MTRsRjg3aFZUcEpXZDJiYWEwWlElMkIlMkJmOHVGMjdJRG5JSVJrQVRWcDNXQWdBT3E3RktOZ1drVERXWWlCU2FJZzFSdEY1eEtvQTdNJTJCU0NDNU9KendhZ3d1QkVYVjNneDlkWUk3T3E3VnRRY1pLdFN2QXNlVndQb1NKZUFEUFZXUkdWdkNyZ1BKMDdHMHlUMGhYeVk3R3JoQVozOVNCdnlLMUlLa1ZCRWZ6QWdYa2U1ZlQzMUtQa0tlVyUyRjk4em5KeGo0ZGhQd2VzQ2lDT0hPTEpNY2xXWDRmOEFoTGdVT3hLc0FmUzlzdiUyRlElM0QlM0Q; X-Lang=en-US; X-TZ-Database-Name=America/Sao_Paulo; _ga=GA1.2.499971693.1747080796; _gid=GA1.2.2113425451.1749749883; __gads=ID=f5d6fcb935d02934:T=1747080798:RT=1749749884:S=ALNI_MbEzTnytdEc_WVuzxHQSFaZkKy_ZQ; __eoi=ID=ed8cdbc75dd84050:T=1747080798:RT=1749749884:S=AA-Afja36jS34gul40Z5mE6Ql6En; FCNEC=%5B%5B%22AKsRol991BcXCpdipkDteDDqcx4Z4ANgsp6sAzMa1yDZxr2f-mKr4Y4qhu9l35q2vyBJZ9emnkbojnTpxktGVM4xdHGNUkCd2_xjpQ_6n8ZFODZpjJX-qExAeZ_4_vMgbYbwFoKuqFUHi1svPBaYORj9DFhmG7WQ0g%3D%3D%22%5D%5D; _ga_8S3H6J5GSR=GS2.1.s1749749882$o15$g1$t1749750415$j48$l0$h0",
    "Referer": "https://www.personality-database.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": null,
  "method": "GET"
});
```

Response:

```json
{
    "data": {
        "count": 4,
        "cursor": {
            "limit": 0,
            "nextCursor": ""
        },
        "results": [
            {
                "subcatID": "137",
                "subcategory": "Dragon Ball Z",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Dragon Ball Z"
                },
                "id": "5164",
                "name": "Android 18 (Lazuli)",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/ca38e77f/profile_images/256eca2b0a644d96acbf8004bad9ffbe.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                },
                "subcategories": [
                    {
                        "id": "137",
                        "name": "Dragon Ball Z",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Dragon Ball Z"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ISTP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "8w9"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Android 18 (Lazuli)"
                },
                "propertyID": "2",
                "categoryID": "8",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "beenVotedByMe": false,
                "voteCount": 252,
                "beenSavedByMe": false,
                "savedCount": 513,
                "beenCommentedByMe": false,
                "commentCount": 26,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=5164",
                "topAnalysis": {
                    "type": "analysis",
                    "id": "3179897",
                    "content": "She and 17 seems very ISTP as an estereotype but i don'tsee Ti that clearly.",
                    "functionList": null
                },
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "3887",
                "subcategory": "Dragon Ball Z (Abridged)",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Dragon Ball Z (Abridged)"
                },
                "id": "38522",
                "name": "Android #18 (TFS DBZ Abridged)",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/d0dc7cc6/profile_images/af05cd015f604d62a3ebe5412ac9d00e.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                },
                "subcategories": [
                    {
                        "id": "3887",
                        "name": "Dragon Ball Z (Abridged)",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Dragon Ball Z (Abridged)"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ISTP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "9w8"
                    }
                ],
                "allowVoting": true,
                "propertyID": "2",
                "categoryID": "8",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "beenVotedByMe": false,
                "voteCount": 7,
                "beenSavedByMe": false,
                "savedCount": 4,
                "beenCommentedByMe": false,
                "commentCount": 0,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=38522",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "32986",
                "subcategory": "Dragon Ball GT",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Dragon Ball GT"
                },
                "id": "1602201",
                "name": "Android 18 (Lazuli)",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/26c0c9e9/profile_images/3d76911cc3e0485cae0cc4e42e5a5b08.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/b2fe2f0d/category_icon_v2/cat_8.png"
                },
                "subcategories": [
                    {
                        "id": "32986",
                        "name": "Dragon Ball GT",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Dragon Ball GT"
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ESTP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": "7w8"
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Android 18 (Lazuli)"
                },
                "propertyID": "2",
                "categoryID": "8",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "beenVotedByMe": false,
                "voteCount": 5,
                "beenSavedByMe": false,
                "savedCount": 3,
                "beenCommentedByMe": false,
                "commentCount": 0,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=1602201",
                "showProfileReaction": false,
                "profileReactions": null
            },
            {
                "subcatID": "44185",
                "subcategory": "Dragonball Multiverse ",
                "subcatI18n": {
                    "detectedLanguage": "en",
                    "en": "Dragonball Multiverse "
                },
                "id": "1702683",
                "name": "Android 18 (Lazuli)",
                "image": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-images-prod/8b809285/profile_images/17651344771d441fb4416b5a87920f90.png"
                },
                "catIcon": {
                    "picURL": "https://static1.personalitydatabase.net/2/pdb-web-static/62742b63/category_icon_v2/cat_26.png"
                },
                "subcategories": [
                    {
                        "id": "44185",
                        "name": "Dragonball Multiverse ",
                        "image": null,
                        "catIcon": null,
                        "i18n": {
                            "detectedLanguage": "en",
                            "en": "Dragonball Multiverse "
                        }
                    }
                ],
                "personalities": [
                    {
                        "system": "Four Letter",
                        "personality": "ISTP"
                    },
                    {
                        "system": "Enneagram",
                        "personality": ""
                    }
                ],
                "allowVoting": true,
                "i18n": {
                    "detectedLanguage": "en",
                    "en": "Android 18 (Lazuli)"
                },
                "propertyID": "2",
                "categoryID": "26",
                "isMeme": false,
                "isCharacter": true,
                "isCelebrity": false,
                "beenVotedByMe": false,
                "voteCount": 1,
                "beenSavedByMe": false,
                "savedCount": 0,
                "beenCommentedByMe": false,
                "commentCount": 0,
                "chemistryLink": "https://styx.personality-database.com/chemistry?to_type=profile\u0026to_id=1702683",
                "showProfileReaction": false,
                "profileReactions": null
            }
        ]
    },
    "error": {
        "code": "S20000",
        "message": "OK",
        "details": {}
    }
}
```
Create interfaces for the response types and a single service in angular to fetch these data