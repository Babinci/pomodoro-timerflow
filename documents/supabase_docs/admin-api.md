1 | Python Reference v2.0
   2 | 
   3 | # Python Client Library
   4 | 
   5 | supabase-py [View on GitHub](https://github.com/supabase/supabase-py)
   6 | 
   7 | This reference documents every object and method available in Supabase's Python library, [supabase-py](https://github.com/supabase/supabase-py). You can use supabase-py to interact with your Postgres database, listen to database changes, invoke Deno Edge Functions, build login and user management functionality, and manage large files.
   8 | 
   9 | * * *
  10 | 
  11 | ## Installing
  12 | 
  13 | ### Install with PyPi [\#](https://supabase.com/docs/reference/python/admin-api\#install-with-pypi)
  14 | 
  15 | You can install supabase-py via the terminal. (for Python > 3.8)
  16 | 
  17 | PIPConda
  18 | 
  19 | ```python
  20 | 
  21 | pip install supabase
  22 | ```
  23 | 
  24 | * * *
  25 | 
  26 | ## Initializing
  27 | 
  28 | You can initialize a new Supabase client using the `create_client()` method.
  29 | 
  30 | The Supabase client is your entrypoint to the rest of the Supabase functionality and is the easiest way to interact with everything we offer within the Supabase ecosystem.
  31 | 
  32 | ### Parameters
  33 | 
  34 | - supabase\_urlRequiredstring
  35 | 
  36 | 
  37 | 
  38 | The unique Supabase URL which is supplied when you create a new project in your project dashboard.
  39 | 
  40 | - supabase\_keyRequiredstring
  41 | 
  42 | 
  43 | 
  44 | The unique Supabase Key which is supplied when you create a new project in your project dashboard.
  45 | 
  46 | - optionsOptionalClientOptions
  47 | 
  48 | 
  49 | 
  50 | Options to change the Auth behaviors.
  51 | 
  52 | 
  53 | 
  54 | Details
  55 | 
  56 | 
  57 | create\_client()With timeout option
  58 | 
  59 | ```python
  60 | import os
  61 | from supabase import create_client, Client
  62 | 
  63 | url: str = os.environ.get("SUPABASE_URL")
  64 | key: str = os.environ.get("SUPABASE_KEY")
  65 | supabase: Client = create_client(url, key)
  66 | ```
  67 | 
  68 | * * *
  69 | 
  70 | ## Fetch data
  71 | 
  72 | - By default, Supabase projects return a maximum of 1,000 rows. This setting can be changed in your project's [API settings](https://supabase.com/dashboard/project/_/settings/api). It's recommended that you keep it low to limit the payload size of accidental or malicious requests. You can use `range()` queries to paginate through your data.
  73 | - `select()` can be combined with [Filters](https://supabase.com/docs/reference/python/using-filters)
  74 | - `select()` can be combined with [Modifiers](https://supabase.com/docs/reference/python/using-modifiers)
  75 | - `apikey` is a reserved keyword if you're using the [Supabase Platform](https://supabase.com/docs/guides/platform) and [should be avoided as a column name](https://github.com/supabase/supabase/issues/5465).
  76 | 
  77 | ### Parameters
  78 | 
  79 | - columnsOptionalstring
  80 | 
  81 | 
  82 | 
  83 | The columns to retrieve, defaults to `*`.
  84 | 
  85 | - countOptionalCountMethod
  86 | 
  87 | 
  88 | 
  89 | The property to use to get the count of rows returned.
  90 | 
  91 | 
  92 | Getting your dataSelecting specific columnsQuery referenced tablesQuery referenced tables through a join tableQuery the same referenced table multiple timesFiltering through referenced tablesQuerying referenced table with countQuerying with count optionQuerying JSON dataQuerying referenced table with inner joinSwitching schemas per query
  93 | 
  94 | ```python
  95 | 
  96 | response = (
  97 |     supabase.table("planets")
  98 |     .select("*")
  99 |     .execute()
 100 | )
 101 | ```
 102 | 
 103 | 
 104 | * * *
 105 | 
 106 | ## Insert data
 107 | 
 108 | ### Parameters
 109 | 
 110 | - jsonRequireddict, list
 111 | 
 112 | 
 113 | 
 114 | The values to insert. Pass an dict to insert a single row or an list to insert multiple rows.
 115 | 
 116 | - countOptionalCountMethod
 117 | 
 118 | 
 119 | 
 120 | The property to use to get the count of rows returned.
 121 | 
 122 | - returningOptionalReturnMethod
 123 | 
 124 | 
 125 | 
 126 | Either 'minimal' or 'representation'. Defaults to 'representation'.
 127 | 
 128 | - default\_to\_nullOptionalbool
 129 | 
 130 | 
 131 | 
 132 | Make missing fields default to `null`. Otherwise, use the default value for the column. Only applies for bulk inserts.
 133 | 
 134 | 
 135 | Create a recordBulk create
 136 | 
 137 | ```python
 138 | 
 139 | response = (
 140 |     supabase.table("planets")
 141 |     .insert({"id": 1, "name": "Pluto"})
 142 |     .execute()
 143 | )
 144 | ```
 145 | 
 146 | 
 147 | * * *
 148 | 
 149 | ## Update data
 150 | 
 151 | - `update()` should always be combined with [Filters](https://supabase.com/docs/reference/python/using-filters) to target the item(s) you wish to update.
 152 | 
 153 | ### Parameters
 154 | 
 155 | - jsonRequireddict, list
 156 | 
 157 | 
 158 | 
 159 | The values to insert. Pass an dict to insert a single row or an list to insert multiple rows.
 160 | 
 161 | - countOptionalCountMethod
 162 | 
 163 | 
 164 | 
 165 | The property to use to get the count of rows returned.
 166 | 
 167 | 
 168 | Updating your dataUpdating JSON data
 169 | 
 170 | ```python
 171 | 
 172 | response = (
 173 |     supabase.table("instruments")
 174 |     .update({"name": "piano"})
 175 |     .eq("id", 1)
 176 |     .execute()
 177 | )
 178 | ```
 179 | 
 180 | 
 181 | * * *
 182 | 
 183 | ## Upsert data
 184 | 
 185 | - Primary keys must be included in the `values` dict to use upsert.
 186 | 
 187 | ### Parameters
 188 | 
 189 | - jsonRequireddict, list
 190 | 
 191 | 
 192 | 
 193 | The values to insert. Pass an dict to insert a single row or an list to insert multiple rows.
 194 | 
 195 | - countOptionalCountMethod
 196 | 
 197 | 
 198 | 
 199 | The property to use to get the count of rows returned.
 200 | 
 201 | - returningOptionalReturnMethod
 202 | 
 203 | 
 204 | 
 205 | Either 'minimal' or 'representation'. Defaults to 'representation'.
 206 | 
 207 | - ignore\_duplicatesOptionalbool
 208 | 
 209 | 
 210 | 
 211 | Whether duplicate rows should be ignored.
 212 | 
 213 | - on\_conflictOptionalstring
 214 | 
 215 | 
 216 | 
 217 | Specified columns to be made to work with UNIQUE constraint.
 218 | 
 219 | - default\_to\_nullOptionalbool
 220 | 
 221 | 
 222 | 
 223 | Make missing fields default to `null`. Otherwise, use the default value for the column. Only applies for bulk inserts.
 224 | 
 225 | 
 226 | Upsert your dataBulk Upsert your dataUpserting into tables with constraints
 227 | 
 228 | ```python
 229 | 
 230 | response = (
 231 |     supabase.table("instruments")
 232 |     .upsert({"id": 1, "name": "piano"})
 233 |     .execute()
 234 | )
 235 | ```
 236 | 
 237 | 
 238 | * * *
 239 | 
 240 | ## Delete data
 241 | 
 242 | - `delete()` should always be combined with [filters](https://supabase.com/docs/reference/python/using-filters) to target the item(s) you wish to delete.
 243 | - If you use `delete()` with filters and you have [RLS](https://supabase.com/docs/learn/auth-deep-dive/auth-row-level-security) enabled, only rows visible through `SELECT` policies are deleted. Note that by default no rows are visible, so you need at least one `SELECT`/ `ALL` policy that makes the rows visible.
 244 | - When using `delete().in_()`, specify an array of values to target multiple rows with a single query. This is particularly useful for batch deleting entries that share common criteria, such as deleting users by their IDs. Ensure that the array you provide accurately represents all records you intend to delete to avoid unintended data removal.
 245 | 
 246 | ### Parameters
 247 | 
 248 | - countOptionalCountMethod
 249 | 
 250 | 
 251 | 
 252 | The property to use to get the count of rows returned.
 253 | 
 254 | - returningOptionalReturnMethod
 255 | 
 256 | 
 257 | 
 258 | Either 'minimal' or 'representation'. Defaults to 'representation'.
 259 | 
 260 | 
 261 | Delete recordsDelete multiple records
 262 | 
 263 | ```python
 264 | 
 265 | response = (
 266 |     supabase.table("countries")
 267 |     .delete()
 268 |     .eq("id", 1)
 269 |     .execute()
 270 | )
 271 | ```
 272 | 
 273 | 
 274 | * * *
 275 | 
 276 | ## Call a Postgres function
 277 | 
 278 | You can call Postgres functions as _Remote Procedure Calls_, logic in your database that you can execute from anywhere. Functions are useful when the logic rarely changes—like for password resets and updates.
 279 | 
 280 | ```flex
 281 | 
 282 | 1
 283 | 2
 284 | 3
 285 | create or replace function hello_world() returns text as $$  select 'Hello world';$$ language sql;
 286 | ```
 287 | 
 288 | ### Parameters
 289 | 
 290 | - fnRequiredcallable
 291 | 
 292 | 
 293 | 
 294 | The stored procedure call to be executed.
 295 | 
 296 | - paramsOptionaldict of any
 297 | 
 298 | 
 299 | 
 300 | Parameters passed into the stored procedure call.
 301 | 
 302 | - getOptionaldict of any
 303 | 
 304 | 
 305 | 
 306 | When set to `true`, `data` will not be returned. Useful if you only need the count.
 307 | 
 308 | - headOptionaldict of any
 309 | 
 310 | 
 311 | 
 312 | When set to `true`, the function will be called with read-only access mode.
 313 | 
 314 | - countOptionalCountMethod
 315 | 
 316 | 
 317 | 
 318 | Count algorithm to use to count rows returned by the function. Only applicable for [set-returning functions](https://www.postgresql.org/docs/current/functions-srf.html). `"exact"`: Exact but slow count algorithm. Performs a `COUNT(*)` under the hood. `"planned"`: Approximated but fast count algorithm. Uses the Postgres statistics under the hood. `"estimated"`: Uses exact count for low numbers and planned count for high numbers.
 319 | 
 320 | 
 321 | Call a Postgres function without argumentsCall a Postgres function with argumentsBulk processingCall a Postgres function with filtersCall a read-only Postgres function
 322 | 
 323 | ```python
 324 | 
 325 | response = (
 326 |     supabase.rpc("hello_world")
 327 |     .execute()
 328 | )
 329 | ```
 330 | 
 331 | Data source
 333 | 
 334 | * * *
 335 | 
 336 | ## Using filters
 337 | 
 338 | Filters allow you to only return rows that match certain conditions.
 339 | 
 340 | Filters can be used on `select()`, `update()`, `upsert()`, and `delete()` queries.
 341 | 
 342 | If a Postgres function returns a table response, you can also apply filters.
 343 | 
 344 | Applying FiltersChainingConditional chainingFilter by values within JSON columnFilter Foreign Tables
 345 | 
 346 | ```python
 347 | 
 348 | # Correct
 349 | response = (
 350 |     supabase.table("instruments")
 351 |     .select("name, section_id")
 352 |     .eq("name", "flute")
 353 |     .execute()
 354 | )
 355 | # Incorrect
 356 | # response = (
 357 | #     supabase.table("instruments")
 358 | #     .eq("name", "flute")
 359 | #     .select("name, section_id")
 360 | #     .execute()
 361 | # )
 362 | ```
 363 | 
 364 | 
 365 | 
 366 | 
 367 | * * *
 368 | 
 369 | ## Column is equal to a value
 370 | 
 371 | Match only rows where `column` is equal to `value`.
 372 | 
 373 | ### Parameters
 374 | 
 375 | - columnRequiredstring
 376 | 
 377 | 
 378 | 
 379 | The column to filter on
 380 | 
 381 | - valueRequiredany
 382 | 
 383 | 
 384 | 
 385 | The value to filter by
 386 | 
 387 | 
 388 | With \`select()\`
 389 | 
 390 | ```flex
 391 | 
 392 | 1
 393 | 2
 394 | 3
 395 | 4
 396 | 5
 397 | 6
 398 | 399 | response = (    supabase.table("planets")    .select("*")    .eq("name", "Earth")    .execute())
 400 | ```
 401 | 
 402 | 
 403 | 
 404 | 
 405 | * * *
 406 | 
 407 | ## Column is not equal to a value
 408 | 
 409 | Match only rows where `column` is not equal to `value`.
 410 | 
 411 | ### Parameters
 412 | 
 413 | - columnRequiredstring
 414 | 
 415 | 
 416 | 
 417 | The column to filter on
 418 | 
 419 | - valueRequiredany
 420 | 
 421 | 
 422 | 
 423 | The value to filter by
 424 | 
 425 | 
 426 | With \`select()\`
 427 | 
 428 | ```flex
 429 | 
 430 | 1
 431 | 2
 432 | 3
 433 | 4
 434 | 5
 435 | 6
 436 | response = (    supabase.table("planets")    .select("*")    .neq("name", "Earth")    .execute())
 437 | ```
 438 | 
 439 | 
 440 | 
 441 | 
 442 | * * *
 443 | 
 444 | ## Column is greater than a value
 445 | 
 446 | Match only rows where `column` is greather than `value`.
 447 | 
 448 | ### Parameters
 449 | 
 450 | - columnRequiredstring
 451 | 
 452 | 
 453 | 
 454 | The column to filter on
 455 | 
 456 | - valueRequiredany
 457 | 
 458 | 
 459 | 
 460 | The value to filter by
 461 | 
 462 | 
 463 | With \`select()\`
 464 | 
 465 | ```flex
 466 | 
 467 | 1
 468 | 2
 469 | 3
 470 | 4
 471 | 5
 472 | 6
 473 | response = (    supabase.table("planets")    .select("*")    .gt("id", 2)    .execute())
 474 | ```
 475 | 
 476 | Data source
 477 | 
 478 | Response
 479 | 
 480 | Notes
 481 | 
 482 | * * *
 483 | 
 484 | ## Column is greater than or equal to a value
 485 | 
 486 | Match only rows where `column` is greater than or equal to `value`.
 487 | 
 488 | ### Parameters
 489 | 
 490 | - columnRequiredstring
 491 | 
 492 | 
 493 | 
 494 | The column to filter on
 495 | 
 496 | - valueRequiredany
 497 | 
 498 | 
 499 | 
 500 | The value to filter by
 501 | 
 502 | 
 503 | With \`select()\`
 504 | 
 505 | ```python
 506 | 
 507 | response = (
 508 |     supabase.table("planets")
 509 |     .select("*")
 510 |     .gte("id", 2)
 511 |     .execute()
 512 | )
 513 | ```
 514 | 
 515 | 
 516 | 
 517 | 
 518 | * * *
 519 | 
 520 | ## Column is less than a value
 521 | 
 522 | Match only rows where `column` is less than `value`.
 523 | 
 524 | ### Parameters
 525 | 
 526 | - columnRequiredstring
 527 | 
 528 | 
 529 | 
 530 | The column to filter on
 531 | 
 532 | - valueRequiredany
 533 | 
 534 | 
 535 | 
 536 | The value to filter by
 537 | 
 538 | 
 539 | With \`select()\`
 540 | 
 541 | ```flex
 542 | 
 543 | 1
 544 | 2
 545 | 3
 546 | 4
 547 | 5
 548 | 6
 549 | response = (    supabase.table("planets")    .select("*")    .lt("id", 2)    .execute())
 550 | ```
 551 | 
 552 | Data source
 553 | 
 554 | Response
 555 | 
 556 | * * *
 557 | 
 558 | * * *
 559 | 
 560 | ## Column is less than or equal to a value
 561 | 
 562 | ### Parameters
 563 | 
 564 | - columnRequiredstring
 565 | 
 566 | 
 567 | 
 568 | The column to filter on
 569 | 
 570 | - valueRequiredany
 571 | 
 572 | 
 573 | 
 574 | The value to filter by
 575 | 
 576 | 
 577 | With \`select()\`
 578 | 
 579 | ```flex
 580 | 
 581 | 1
 582 | 2
 583 | 3
 584 | 4
 585 | 5
 586 | 6
 587 | response = (    supabase.table("planets")    .select("*")    .lte("id", 2)    .execute())
 588 | ```
 589 | 
 590 | Data source
 591 | 
 592 | Response
 593 | 
 594 | * * *
 595 | 
 596 | ## Column matches a pattern
 597 | 
 598 | Match only rows where `column` matches `pattern` case-sensitively.
 599 | 
 600 | ### Parameters
 601 | 
 602 | - columnRequiredstring
 603 | 
 604 | 
 605 | 
 606 | The name of the column to apply a filter on
 607 | 
 608 | - patternRequiredstring
 609 | 
 610 | 
 611 | 
 612 | The pattern to match by
 613 | 
 614 | 
 615 | With \`select()\`
 616 | 
 617 | ```python
 618 | 
 619 | response = (
 620 |     supabase.table("planets")
 621 |     .select("*")
 622 |     .like("name", "%Ea%")
 623 |     .execute()
 624 | )
 625 | ```
 626 | 
 627 | 
 628 | * * *
 629 | 
 630 | ## Column matches a case-insensitive pattern
 631 | 
 632 | Match only rows where `column` matches `pattern` case-insensitively.
 633 | 
 634 | ### Parameters
 635 | 
 636 | - columnRequiredstring
 637 | 
 638 | 
 639 | 
 640 | The name of the column to apply a filter on
 641 | 
 642 | - patternRequiredstring
 643 | 
 644 | 
 645 | 
 646 | The pattern to match by
 647 | 
 648 | 
 649 | With \`select()\`
 650 | 
 651 | ```python
 652 | 
 653 | response = (
 654 |     supabase.table("planets")
 655 |     .select("*")
 656 |     .ilike("name", "%ea%")
 657 |     .execute()
 658 | )
 659 | ```
 660 | 
 661 | Data source
 662 | 
 663 | Response
 664 | 
 665 | * * *
 666 | 
 667 | ## Column is a value
 668 | 
 669 | Match only rows where `column` IS `value`.
 670 | 
 671 | ### Parameters
 672 | 
 673 | - columnRequiredstring
 674 | 
 675 | 
 676 | 
 677 | The name of the column to apply a filter on
 678 | 
 679 | - valueRequirednull \| boolean
 680 | 
 681 | 
 682 | 
 683 | The value to match by
 684 | 
 685 | 
 686 | Checking for nullness, True or False
 687 | 
 688 | ```python
 689 | 
 690 | response = (
 691 |     supabase.table("planets")
 692 |     .select("*")
 693 |     .is_("name", "null")
 694 |     .execute()
 695 | )
 696 | ```
 697 | 
 698 | 
 699 | Notes
 700 | 
 701 | * * *
 702 | 
 703 | ## Column is in an array
 704 | 
 705 | Match only rows where `column` is included in the `values` array.
 706 | 
 707 | ### Parameters
 708 | 
 709 | - columnRequiredstring
 710 | 
 711 | 
 712 | 
 713 | The column to filter on
 714 | 
 715 | - valuesRequiredarray
 716 | 
 717 | 
 718 | 
 719 | The values to filter by
 720 | 
 721 | 
 722 | With \`select()\`
 723 | 
 724 | ```python
 725 | 
 726 | response = (
 727 |     supabase.table("planets")
 728 |     .select("*")
 729 |     .in_("name", ["Earth", "Mars"])
 730 |     .execute()
 731 | )
 732 | ```
 733 | 
 734 | Data source
 735 | 
 736 | Response
 737 | 
 738 | * * *
 739 | 
 740 | ## Column contains every element in a value
 741 | 
 742 | Only relevant for jsonb, array, and range columns. Match only rows where `column` contains every element appearing in `value`.
 743 | 
 744 | ### Parameters
 745 | 
 746 | - columnRequiredstring
 747 | 
 748 | 
 749 | 
 750 | The column to filter on
 751 | 
 752 | - valuesRequiredobject
 753 | 
 754 | 
 755 | 
 756 | The jsonb, array, or range value to filter with
 757 | 
 758 | 
 759 | On array columnsOn range columnsOn \`jsonb\` columns
 760 | 
 761 | ```python
 762 | 
 763 | response = (
 764 |     supabase.table("issues")
 765 |     .select("*")
 766 |     .contains("tags", ["is:open", "priority:low"])
 767 |     .execute()
 768 | )
 769 | ```
 770 | 
 771 | Data source
 772 | 
 773 | Response
 774 | 
 775 | * * *
 776 | 
 777 | ## Contained by value
 778 | 
 779 | Only relevant for jsonb, array, and range columns. Match only rows where every element appearing in `column` is contained by `value`.
 780 | 
 781 | ### Parameters
 782 | 
 783 | - columnRequiredstring
 784 | 
 785 | 
 786 | 
 787 | The jsonb, array, or range column to filter on
 788 | 
 789 | - valueRequiredobject
 790 | 
 791 | 
 792 | 
 793 | The jsonb, array, or range value to filter with
 794 | 
 795 | 
 796 | On array columnsOn range columnsOn \`jsonb\` columns
 797 | 
 798 | ```
 799 | 
 800 | response = (
 801 |     supabase.table("classes")
 802 |     .select("name")
Response

* * *

## Match a string

Only relevant for text and tsvector columns. Match only rows where `column` matches the query string in `query`.

- For more information, see [Postgres full text search](https://supabase.com/docs/guides/database/full-text-search).

### Parameters

- columnRequiredstring



The text or tsvector column to filter on

- queryRequiredstring



The query text to match with

- optionsOptionalobject



Named parameters



Details


Text searchBasic normalizationFull normalizationWebsearch

```python

response = (
    supabase.table("texts")
    .select("content")
    .text_search(
        "content",
        "'eggs' & 'ham'",
        options={"config": "english"},
    )
    .execute()
)
```

Data source

Response

* * *

## Match an associated value

Match only rows where each column in `query` keys is equal to its associated value. Shorthand for multiple `.eq()` s.

### Parameters

- queryRequireddict



The object to filter with, with column names as keys mapped to their filter values


With \`select()\`

```flex

1
2
3
4
5
6
response = (    supabase.table("planets")    .select("*")    .match({"id": 2, "name": "Earth"})    .execute())
```

Data source

Response

* * *

## Don't match the filter

Match only rows which doesn't satisfy the filter. `not_` expects you to use the raw PostgREST syntax for the filter values.

```python

.not_.in_('id', '(5,6,7)')  # Use `()` for `in` filter.
.not_.contains('arraycol', '{"a","b"}')  # Use `{}` for array values
```

With \`select()\`

```flex

1
2
3
4
5
6
response = (    supabase.table("planets")    .select("*")    .not_.is_("name", "null")    .execute())
```

Data source

Response

* * *

## Match at least one filter

or\_() expects you to use the raw PostgREST syntax for the filter names and values.

```python

.or_('id.in.(5,6,7), arraycol.cs.{"a","b"}')  # Use `()` for `in` filter, `{}` for array values and `cs` for `contains()`
.or_('id.in.(5,6,7), arraycol.cd.{"a","b"}')  # Use `cd` for `containedBy()`
```

### Parameters

- filtersRequiredstring



The filters to use, following PostgREST syntax

- reference\_tableOptionalstring



Set this to filter on referenced tables instead of the parent table


With \`select()\`Use \`or\` with \`and\`Use \`or\` on referenced tables

```flex

1
2
3
4
5
6
response = (    supabase.table("planets")    .select("name")    .or_("id.eq.2,name.eq.Mars")    .execute())
```

Data source

Response

* * *

## Match the filter

filter() expects you to use the raw PostgREST syntax for the filter values.

```flex

1
2
.filter('id', 'in', '(5,6,7)')  # Use `()` for `in` filter.filter('arraycol', 'cs', '{"a","b"}')  # Use `cs` for `contains()`, `{}` for array values
```

### Parameters

- columnRequiredstring



The column to filter on

- operatorOptionalstring



The operator to filter with, following PostgREST syntax

- valueOptionalany



The value to filter with, following PostgREST syntax


With \`select()\`On a foreign table

```flex

1
2
3
4
5
6
response = (    supabase.table("planets")    .select("*")    .filter("name", "in", '("Mars","Tatooine")')    .execute())
```

Data source

Response

* * *

## Using modifiers

Filters work on the row level—they allow you to return rows that only match certain conditions without changing the shape of the rows. Modifiers are everything that don't fit that definition—allowing you to change the format of the response (e.g., returning a CSV string).

Modifiers must be specified after filters. Some modifiers only apply for queries that return rows (e.g., `select()` or `rpc()` on a function that returns a table response).

* * *

## Order the results

Order the query result by `column`.

### Parameters

- columnRequiredstring



The column to order by

- descOptionalbool



Whether the rows should be ordered in descending order or not.

- foreign\_tableOptionalstring



Foreign table name whose results are to be ordered.

- nullsfirstOptionalbool



Order by showing nulls first


With \`select()\`On a foreign tableOrder parent table by a referenced table

```flex

1
2
3
4
5
6
response = (    supabase.table("planets")    .select("*")    .order("name", desc=True)    .execute())
```

Data source

Response

* * *

## Limit the number of rows returned

### Parameters

- sizeRequirednumber



The maximum number of rows to return

- foreign\_tableOptionalstring



Set this to limit rows of foreign tables instead of the parent table.


With \`select()\`On a foreign table

```python

response = (
    supabase.table("planets")
    .select("name")
    .limit(1)
    .execute()
)
```

Data source

Response

* * *

## Limit the query to a range

Limit the query result by starting at an offset ( `start`) and ending at the offset ( `end`). Only records within this range are returned. This respects the query order and if there is no order clause the range could behave unexpectedly.

The `start` and `end` values are 0-based and inclusive: `range(1, 3)` will include the second, third and fourth rows of the query.

### Parameters

- startRequirednumber



The starting index from which to limit the result.

- endRequirednumber



The last index to which to limit the result.

- foreign\_tableOptionalstring



Set this to limit rows of foreign tables instead of the parent table.


With \`select()\`On a foreign table

```flex

1
2
3
4
5
6
response = (    supabase.table("planets")    .select("name")    .range(0, 1)    .execute())
```

Data source

Response

* * *

## Retrieve one row of data

Return `data` as a single object instead of an array of objects.

With \`select()\`

```flex

1
2
3
4
5
6
7
response = (    supabase.table("planets")    .select("name")    .limit(1)    .single()    .execute())
```

Data source

Response

* * *

## Retrieve zero or one row of data

Return `data` as a single object instead of an array of objects.

With \`select()\`

```flex

1
2
3
4
5
6
7
response = (    supabase.table("planets")    .select("*")    .eq("name", "Earth")    .maybe_single()    .execute())
```

Data source

Response

* * *

## Retrieve as a CSV

Return `data` as a string in CSV format.

Return data as CSV

```flex

1
2
3
4
5
6
response = (    supabase.table("planets")    .select("*")    .csv()    .execute())
```

Data source

Response

Notes

* * *

## Using explain

For debugging slow queries, you can get the [Postgres `EXPLAIN` execution plan](https://www.postgresql.org/docs/current/sql-explain.html) of a query using the `explain()` method. This works on any query, even for `rpc()` or writes.

Explain is not enabled by default as it can reveal sensitive information about your database. It's best to only enable this for testing environments but if you wish to enable it for production you can provide additional protection by using a `pre-request` function.

Follow the [Performance Debugging Guide](https://supabase.com/docs/guides/database/debugging-performance) to enable the functionality on your project.

### Parameters

- walOptionalboolean



If `true`, include information on WAL record generation.

- verboseOptionalboolean



If `true`, the query identifier will be returned and `data` will include the output columns of the query.

- settingsOptionalboolean



If `true`, include information on configuration parameters that affect query planning.

- formatOptionalboolean



The format of the output, can be `"text"` (default) or `"json"`.

- formatOptional"text" \| "json"



The format of the output, can be `"text"` (default) or `"json"`.

- buffersOptionalboolean



If `true`, include information on buffer usage.

- analyzeOptionalboolean



If `true`, the query will be executed and the actual run time will be returned.


Get the execution planGet the execution plan with analyze and verbose

```flex

1
2
3
4
5
6
response = (    supabase.table("planets")    .select("*")    .explain()    .execute())
```

Data source

Response

Notes

* * *

## Overview

- The auth methods can be accessed via the `supabase.auth` namespace.
- By default, the supabase client sets `persist_session` to true and attempts to store the session in memory.
- Any email links and one-time passwords (OTPs) sent have a default expiry of 24 hours. We have the following [rate limits](https://supabase.com/docs/guides/platform/going-into-prod#auth-rate-limits) in place to guard against brute force attacks.
- The expiry of an access token can be set in the "JWT expiry limit" field in [your project's auth settings](https://supabase.com/dashboard/project/_/settings/auth). A refresh token never expires and can only be used once.

* * *

## Create a new user

- By default, the user needs to verify their email address before logging in. To turn this off, disable **Confirm email** in [your project](https://supabase.com/dashboard/project/_/auth/providers).
- **Confirm email** determines if users need to confirm their email address after signing up.

  - If **Confirm email** is enabled, a `user` is returned but `session` is null.
  - If **Confirm email** is disabled, both a `user` and a `session` are returned.
- By default, when the user confirms their email address, they are redirected to the [`SITE_URL`](https://supabase.com/docs/guides/auth/redirect-urls). You can modify your `SITE_URL` or add additional redirect URLs in [your project](https://supabase.com/dashboard/project/_/auth/url-configuration).
- If sign\_up() is called for an existing confirmed user:
  - When both **Confirm email** and **Confirm phone** (even when phone provider is disabled) are enabled in [your project](https://supabase.com/dashboard/project/_/auth/providers), an obfuscated/fake user object is returned.
  - When either **Confirm email** or **Confirm phone** (even when phone provider is disabled) is disabled, the error message, `User already registered` is returned.
- To fetch the currently logged-in user, refer to [`get_user()`](https://supabase.com/docs/reference/python/auth-getuser).

### Parameters

- credentialsRequiredSignUpWithPasswordCredentials

Details


Sign up with an email and passwordSign up with a phone number and password (SMS)Sign up with a phone number and password (whatsapp)Sign up with additional user metadataSign up with a redirect URL

```flex

1
2
3
4
5
6
response = supabase.auth.sign_up(    {        "email": "email@example.com",         "password": "password",    })
```

Response

* * *

## Create an anonymous user

- Returns an anonymous user
- It is recommended to set up captcha for anonymous sign-ins to prevent abuse. You can pass in the captcha token in the `options` param.

### Parameters

- credentialsRequiredSignInAnonymouslyCredentials

Details


Create an anonymous userCreate an anonymous user with custom user metadata

```flex

1
2
3
response = supabase.auth.sign_in_anonymously(    {"options": {"captcha_token": ""}})
```

Response

* * *

## Sign in a user

Log in an existing user with an email and password or phone and password.

- Requires either an email and password or a phone number and password.

### Parameters

- credentialsRequiredSignInWithPasswordCredentials

Details


Sign in with email and passwordSign in with phone and password

```flex

1
2
3
4
5
6
response = supabase.auth.sign_in_with_password(    {        "email": "email@example.com",         "password": "example-password",    })
```

Response

* * *

## Sign in with ID Token

Allows signing in with an OIDC ID token. The authentication provider used should be enabled and configured.

### Parameters

- credentialsRequiredSignInWithIdTokenCredentials

Details


Sign In using ID Token

```flex

1
2
3
4
5
6
response = supabase.auth.sign_in_with_id_token(    {        "provider": "google",         "token": "your-id-token",    })
```

Response

* * *

## Sign in a user through OTP

- Requires either an email or phone number.
- This method is used for passwordless sign-ins where a OTP is sent to the user's email or phone number.
- If the user doesn't exist, `sign_in_with_otp()` will signup the user instead. To restrict this behavior, you can set `should_create_user` in `SignInWithPasswordlessCredentials.options` to `false`.
- If you're using an email, you can configure whether you want the user to receive a magiclink or a OTP.
- If you're using phone, you can configure whether you want the user to receive a OTP.
- The magic link's destination URL is determined by the [`SITE_URL`](https://supabase.com/docs/guides/auth/redirect-urls).
- See [redirect URLs and wildcards](https://supabase.com/docs/guides/auth/redirect-urls#use-wildcards-in-redirect-urls) to add additional redirect URLs to your project.
- Magic links and OTPs share the same implementation. To send users a one-time code instead of a magic link, [modify the magic link email template](https://supabase.com/dashboard/project/_/auth/templates) to include `{{ .Token }}` instead of `{{ .ConfirmationURL }}`.

### Parameters

- credentialsRequiredSignInWithPasswordCredentials

Details


Sign in with emailSign in with SMS OTPSign in with WhatsApp OTP

```flex

1
2
3
4
5
6
7
8
response = supabase.auth.sign_in_with_otp(    {        "email": "email@example.com",        "options": {            "email_redirect_to": "https://example.com/welcome",        },    })
```

Response

Notes

* * *

## Sign in a user through OAuth

- This method is used for signing in using a third-party provider.
- Supabase supports many different [third-party providers](https://supabase.com/docs/guides/auth#configure-third-party-providers).

### Parameters

- credentialsRequiredSignInWithOAuthCredentials

Details


Sign in using a third-party providerSign in using a third-party provider with redirectSign in with scopes

```flex

1
2
3
response = supabase.auth.sign_in_with_oauth(    {"provider": "github"})
```

* * *

## Sign in a user through SSO

- Before you can call this method you need to [establish a connection](https://supabase.com/docs/guides/auth/sso/auth-sso-saml#managing-saml-20-connections) to an identity provider. Use the [CLI commands](https://supabase.com/docs/reference/cli/supabase-sso) to do this.
- If you've associated an email domain to the identity provider, you can use the `domain` property to start a sign-in flow.
- In case you need to use a different way to start the authentication flow with an identity provider, you can use the `provider_id` property. For example:

  - Mapping specific user email addresses with an identity provider.
  - Using different hints to identity the identity provider to be used by the user, like a company-specific page, IP address or other tracking information.

### Parameters

- paramsRequiredSignInWithSSOCredentials

Details


Sign in with email domainSign in with provider UUID

```flex

1
2
3
response = supabase.auth.sign_in_with_sso(    {"domain": "company.com"})
```

Response

Notes

* * *

## Sign out a user

- In order to use the `sign_out()` method, the user needs to be signed in first.
- By default, `sign_out()` uses the global scope, which signs out all other sessions that the user is logged into as well.
- Since Supabase Auth uses JWTs for authentication, the access token JWT will be valid until it's expired. When the user signs out, Supabase revokes the refresh token and deletes the JWT from the client-side. This does not revoke the JWT and it will still be valid until it expires.

### Parameters

- optionsOptionalSignOutOptions

Details


Sign out

```flex

1
response = supabase.auth.sign_out()
```

* * *

## Send a password reset request

- The password reset flow consist of 2 broad steps: (i) Allow the user to login via the password reset link; (ii) Update the user's password.
- The `reset_password_for_email()` only sends a password reset link to the user's email. To update the user's password, see [`update_user()`](https://supabase.com/docs/reference/python/auth-updateuser).
- When the user clicks the reset link in the email they are redirected back to your application. You can configure the URL that the user is redirected to with the `redirectTo` parameter. See [redirect URLs and wildcards](https://supabase.com/docs/reference/python/docs/guides/auth/redirect-urls#use-wildcards-in-redirect-urls) to add additional redirect URLs to your project.
- After the user has been redirected successfully, prompt them for a new password and call `update_user()`:

```flex

1
2
3
response = supabase.auth.update_user(    {"password": new_password})
```

### Parameters

- emailRequiredstring



The email address of the user.

- optionsOptionalobject

Details


Reset password

```flex

1
2
3
4
5
6
supabase.auth.reset_password_for_email(    email,    {        "redirect_to": "https://example.com/update-password",    })
```

* * *

## Verify and log in through OTP

- The `verify_otp` method takes in different verification types. If a phone number is used, the type can either be `sms` or `phone_change`. If an email address is used, the type can be one of the following: `email`, `recovery`, `invite` or `email_change` ( `signup` and `magiclink` types are deprecated).
- The verification type used should be determined based on the corresponding auth method called before `verify_otp` to sign up / sign-in a user.
- The `TokenHash` is contained in the [email templates](https://supabase.com/docs/guides/auth/auth-email-templates) and can be used to sign in. You may wish to use the hash with Magic Links for the PKCE flow for Server Side Auth. See [this guide](https://supabase.com/docs/guides/auth/server-side/email-based-auth-with-pkce-flow-for-ssr) for more details.

### Parameters

- paramsRequiredVerifyOtpParams

Details


Verify Signup One-Time Password (OTP)Verify SMS One-Time Password (OTP)Verify Email Auth (Token Hash)

```flex

1
2
3
4
5
6
7
response = supabase.auth.verify_otp(    {        "email": "email@example.com",         "token": "123456",         "type": "email",    })
```

Response

* * *

## Retrieve a session

- This method retrieves the current local session (i.e in memory).
- The session contains a signed JWT and unencoded session data.
- Since the unencoded session data is retrieved from the local storage medium, **do not** rely on it as a source of trusted data on the server. It could be tampered with by the sender. If you need verified, trustworthy user data, call [`get_user`](https://supabase.com/docs/reference/python/auth-getuser) instead.
- If the session has an expired access token, this method will use the refresh token to get a new session.

Get the session data

```flex

1
response = supabase.auth.get_session()
```

Response

* * *

## Retrieve a new session

Returns a new session, regardless of expiry status. Takes in an optional refresh token. If not passed in, then refresh\_session() will attempt to retrieve it from get\_session(). If the current session's refresh token is invalid, an error will be thrown.

- This method will refresh the session whether the current one is expired or not.

### Parameters

- refresh\_tokenOptionalstring


Refresh session using the current session

```flex

1
response = supabase.auth.refresh_session()
```

Response

* * *

## Retrieve a user

- This method fetches the user object from the database instead of local session.
- This method is useful for checking if the user is authorized because it validates the user's access token JWT on the server.

### Parameters

- jwtOptionalstring



Takes in an optional access token JWT. If no JWT is provided, the JWT from the current session is used.


Get the logged in user with the current existing sessionGet the logged in user with a custom access token jwt

```flex

1
response = supabase.auth.get_user()
```

Response

* * *

## Update a user

- In order to use the `update_user()` method, the user needs to be signed in first.
- By default, email updates sends a confirmation link to both the user's current and new email. To only send a confirmation link to the user's new email, disable **Secure email change** in your project's [email auth provider settings](https://supabase.com/dashboard/project/_/auth/providers).

Update the email for an authenticated userUpdate the phone number for an authenticated userUpdate the password for an authenticated userUpdate the user's metadataUpdate the user's password with a nonce

```flex

1
2
3
response = supabase.auth.update_user(    {"email": "new@email.com"})
```

Response

Notes

* * *

## Retrieve identities linked to a user

Gets all the identities linked to a user.

- The user needs to be signed in to call `get_user_identities()`.

Returns a list of identities linked to the user

```flex

1
response = supabase.auth.get_user_identities()
```

Response

* * *

## Link an identity to a user

- The **Enable Manual Linking** option must be enabled from your [project's authentication settings](https://supabase.com/dashboard/project/_/settings/auth).
- The user needs to be signed in to call `link_identity()`.
- If the candidate identity is already linked to the existing user or another user, `link_identity()` will fail.
- If `link_identity` is run on the server, you should handle the redirect.

### Parameters

- credentialsRequiredSignInWithOAuthCredentials

Details


Link an identity to a user

```flex

1
2
3
response = supabase.auth.link_identity(    {provider: "github"})
```

Response

* * *

## Unlink an identity from a user

- The **Enable Manual Linking** option must be enabled from your [project's authentication settings](https://supabase.com/dashboard/project/_/settings/auth).
- The user needs to be signed in to call `unlink_identity()`.
- The user must have at least 2 identities in order to unlink an identity.
- The identity to be unlinked must belong to the user.

### Parameters

- identityRequiredUserIdentity

Details


Unlink an identity

```flex

1
2
3
4
5
6
7
8
9
10
# retrieve all identites linked to a userresponse = supabase.auth.get_user_identities()# find the google identitygoogle_identity = list(    filter(lambda identity: identity.provider == "google", res.identities)).pop()# unlink the google identityresponse = supabase.auth.unlink_identity(google_identity)
```

* * *

## Send a password reauthentication nonce

- This method is used together with `updateUser()` when a user's password needs to be updated.
- If you require your user to reauthenticate before updating their password, you need to enable the **Secure password change** option in your [project's email provider settings](https://supabase.com/dashboard/project/_/auth/providers).
- A user is only require to reauthenticate before updating their password if **Secure password change** is enabled and the user **hasn't recently signed in**. A user is deemed recently signed in if the session was created in the last 24 hours.
- This method will send a nonce to the user's email. If the user doesn't have a confirmed email address, the method will send the nonce to the user's confirmed phone number instead.

Send reauthentication nonce

```flex

1
response = supabase.auth.reauthenticate()
```

Notes

* * *

## Resend an OTP

- Resends a signup confirmation, email change or phone change email to the user.
- Passwordless sign-ins can be resent by calling the `sign_in_with_otp()` method again.
- Password recovery emails can be resent by calling the `reset_password_for_email()` method again.
- This method will only resend an email or phone OTP to the user if there was an initial signup, email change or phone change request being made.
- You can specify a redirect url when you resend an email link using the `email_redirect_to` option.

### Parameters

- credentialsRequiredResendCredentials

Details


Resend an email signup confirmationResend a phone signup confirmationResend email change emailResend phone change OTP

```flex

1
2
3
4
5
6
7
8
9
response = supabase.auth.resend(    {        "type": "signup",        "email": "email@example.com",        "options": {            "email_redirect_to": "https://example.com/welcome",        },    })
```

Notes

* * *

## Set the session data

Sets the session data from the current session. If the current session is expired, setSession will take care of refreshing it to obtain a new session. If the refresh token or access token in the current session is invalid, an error will be thrown.

- This method sets the session using an `access_token` and `refresh_token`.
- If successful, a `SIGNED_IN` event is emitted.

### Parameters

- access\_tokenRequiredstring

- refresh\_tokenRequiredstring


Refresh the session

```flex

1
response = supabase.auth.set_session(access_token, refresh_token)
```

Response

Notes

* * *

## Exchange an auth code for a session

Log in an existing user by exchanging an Auth Code issued during the PKCE flow.

- Used when `flow_type` is set to `pkce` in client options.

### Parameters

- auth\_codeRequiredstring


Exchange Auth Code

```flex

1
2
3
response = supabase.auth.exchange_code_for_session(    {"auth_code": "34e770dd-9ff9-416c-87fa-43b31d7ef225"})
```

Response

* * *

## Auth MFA

This section contains methods commonly used for Multi-Factor Authentication (MFA) and are invoked behind the `supabase.auth.mfa` namespace.

Currently, we only support time-based one-time password (TOTP) as the 2nd factor. We don't support recovery codes but we allow users to enroll more than 1 TOTP factor, with an upper limit of 10.

Having a 2nd TOTP factor for recovery frees the user of the burden of having to store their recovery codes somewhere. It also reduces the attack surface since multiple recovery codes are usually generated compared to just having 1 backup TOTP factor.

* * *

## Enroll a factor

- Currently, `totp` is the only supported `factor_type`. The returned `id` should be used to create a challenge.
- To create a challenge, see [`mfa.challenge()`](https://supabase.com/docs/reference/python/auth-mfa-challenge).
- To verify a challenge, see [`mfa.verify()`](https://supabase.com/docs/reference/python/auth-mfa-verify).
- To create and verify a challenge in a single step, see [`mfa.challenge_and_verify()`](https://supabase.com/docs/reference/python/auth-mfa-challengeandverify).

Enroll a time-based, one-time password (TOTP) factor

```flex

1
2
3
4
5
6
response = supabase.auth.mfa.enroll(    {        "factor_type": "totp",        "friendly_name": "your_friendly_name",    })
```

* * *

## Create a challenge

- An [enrolled factor](https://supabase.com/docs/reference/python/auth-mfa-enroll) is required before creating a challenge.
- To verify a challenge, see [`mfa.verify()`](https://supabase.com/docs/reference/python/auth-mfa-verify).

Create a challenge for a factor

```flex

1
2
3
response = supabase.auth.mfa.challenge(    {"factor_id": "34e770dd-9ff9-416c-87fa-43b31d7ef225"})
```

* * *

## Verify a challenge

- To verify a challenge, please [create a challenge](https://supabase.com/docs/reference/python/auth-mfa-challenge) first.

Verify a challenge for a factor

```flex

1
2
3
4
5
6
7
response = supabase.auth.mfa.verify(    {        "factor_id": "34e770dd-9ff9-416c-87fa-43b31d7ef225",        "challenge_id": "4034ae6f-a8ce-4fb5-8ee5-69a5863a7c15",        "code": "123456",    })
```

* * *

## Create and verify a challenge

- An [enrolled factor](https://supabase.com/docs/reference/python/auth-mfa-enroll) is required before invoking `challengeAndVerify()`.
- Executes [`mfa.challenge()`](https://supabase.com/docs/reference/python/auth-mfa-challenge) and [`mfa.verify()`](https://supabase.com/docs/reference/python/auth-mfa-verify) in a single step.

Create and verify a challenge for a factor

```flex

1
2
3
4
5
6
response = supabase.auth.mfa.challenge_and_verify(    {        "factor_id": "34e770dd-9ff9-416c-87fa-43b31d7ef225",        "code": "123456",    })
```

* * *

## Unenroll a factor

Unenroll a factor

```flex

1
2
3
response = supabase.auth.mfa.unenroll(    {"factor_id": "34e770dd-9ff9-416c-87fa-43b31d7ef225"})
```

* * *

## Get Authenticator Assurance Level

- Authenticator Assurance Level (AAL) is the measure of the strength of an authentication mechanism.
- In Supabase, having an AAL of `aal1` refers to having the 1st factor of authentication such as an email and password or OAuth sign-in while `aal2` refers to the 2nd factor of authentication such as a time-based, one-time-password (TOTP).
- If the user has a verified factor, the `next_level` field will return `aal2`, else, it will return `aal1`.

Get the AAL details of a session

```flex

1
response = supabase.auth.mfa.get_authenticator_assurance_level()
```

* * *

## Auth Admin

- Any method under the `supabase.auth.admin` namespace requires a `service_role` key.
- These methods are considered admin methods and should be called on a trusted server. Never expose your `service_role` key in the browser.

Create server-side auth client

```flex

1
2
3
4
5
6
7
8
9
10
11
12
13
14
from supabase import create_clientfrom supabase.lib.client_options import ClientOptionssupabase = create_client(    supabase_url,    service_role_key,    options=ClientOptions(        auto_refresh_token=False,        persist_session=False,    ))# Access auth admin apiadmin_auth_client = supabase.auth.admin
```

* * *

## Retrieve a user

- Fetches the user object from the database based on the user's id.
- The `get_user_by_id()` method requires the user's id which maps to the `auth.users.id` column.

### Parameters

- uidRequiredstring



The user's unique identifier



This function should only be called on a server. Never expose your `service_role` key in the browser.


Fetch the user object using the access\_token jwt

```flex

1
response = supabase.auth.admin.get_user_by_id(1)
```

Response

* * *

## List all users

- Defaults to return 50 users per page.

### Parameters

- paramsOptionalPageParams



An object which supports page and per\_page as numbers, to alter the paginated results.



Details


Get a page of usersPaginated list of users

```flex

1
response = supabase.auth.admin.list_users()
```

* * *

## Create a user

- To confirm the user's email address or phone number, set `email_confirm` or `phone_confirm` to true. Both arguments default to false.
- `create_user()` will not send a confirmation email to the user. You can use [`invite_user_by_email()`](https://supabase.com/docs/reference/python/auth-admin-inviteuserbyemail) if you want to send them an email invite instead.
- If you are sure that the created user's email or phone number is legitimate and verified, you can set the `email_confirm` or `phone_confirm` param to `true`.

### Parameters

- attributesRequiredAdminUserAttributes

Details


With custom user metadataAuto-confirm the user's emailAuto-confirm the user's phone number

```flex

1
2
3
4
5
6
7
response = supabase.auth.admin.create_user(    {        "email": "user@email.com",        "password": "password",        "user_metadata": {"name": "Yoda"},    })
```

Response

* * *

## Delete a user

Delete a user. Requires a `service_role` key.

- The `delete_user()` method requires the user's ID, which maps to the `auth.users.id` column.

### Parameters

- idRequiredstring



The user id you want to remove.

- should\_soft\_deleteOptionalboolean



If true, then the user will be soft-deleted (setting `deleted_at` to the current timestamp and disabling their account while preserving their data) from the auth schema. Defaults to false for backward compatibility.



This function should only be called on a server. Never expose your `service_role` key in the browser.


Removes a user

```flex

1
2
3
supabase.auth.admin.delete_user(    "715ed5db-f090-4b8c-a067-640ecee36aa0")
```

* * *

## Send an email invite link

Sends an invite link to an email address.

- Sends an invite link to the user's email address.
- The `invite_user_by_email()` method is typically used by administrators to invite users to join the application.
- Note that PKCE is not supported when using `invite_user_by_email`. This is because the browser initiating the invite is often different from the browser accepting the invite which makes it difficult to provide the security guarantees required of the PKCE flow.

### Parameters

- emailRequiredstring



The email address of the user.

- optionsOptionalInviteUserByEmailOptions

Details


Invite a user

```flex

1
response = supabase.auth.admin.invite_user_by_email("email@example.com")
```

Response

* * *

## Generate an email link

- The following types can be passed into `generate_link()`: `signup`, `magiclink`, `invite`, `recovery`, `email_change_current`, `email_change_new`, `phone_change`.
- `generate_link()` only generates the email link for `email_change_email` if the **Secure email change** is enabled in your project's [email auth provider settings](https://supabase.com/dashboard/project/_/auth/providers).
- `generate_link()` handles the creation of the user for `signup`, `invite` and `magiclink`.

### Parameters

- paramsRequiredGenerateLinkParams

Details


Generate a signup linkGenerate an invite linkGenerate a magic linkGenerate a recovery linkGenerate links to change current email address

```flex

1
2
3
4
5
6
7
response = supabase.auth.admin.generate_link(    {        "type": "signup",        "email": "email@example.com",        "password": "secret",    })
```

Response

* * *

## Update a user

### Parameters

- uidRequiredstring

- attributesRequiredAdminUserAttributes



The data you want to update.



This function should only be called on a server. Never expose your `service_role` key in the browser.



Details


Updates a user's emailUpdates a user's passwordUpdates a user's metadataUpdates a user's app\_metadataConfirms a user's email addressConfirms a user's phone number

```flex

1
2
3
4
5
6
response = supabase.auth.admin.update_user_by_id(    "11111111-1111-1111-1111-111111111111",    {        "email": "new@email.com",    })
```

Response

* * *

## Delete a factor for a user

Deletes a factor on a user. This will log the user out of all active sessions if the deleted factor was verified.

### Parameters

- paramsRequiredAuthMFAAdminDeleteFactorParams

Details


Delete a factor for a user

```flex

1
2
3
4
5
6
response = supabase.auth.admin.mfa.delete_factor(    {        "id": "34e770dd-9ff9-416c-87fa-43b31d7ef225",        "user_id": "a89baba7-b1b7-440f-b4bb-91026967f66b"    })
```

Response

* * *

## Invokes a Supabase Edge Function.

Invoke a Supabase Function.

- Requires an Authorization header.
- When you pass in a body to your function, we automatically attach the Content-Type header for `Blob`, `ArrayBuffer`, `File`, `FormData` and `String`. If it doesn't match any of these types we assume the payload is `json`, serialise it and attach the `Content-Type` header as `application/json`. You can override this behaviour by passing in a `Content-Type` header of your own.

Basic invocationError handlingPassing custom headers

```flex

1
2
3
4
5
6
response = supabase.functions.invoke(    "hello-world",     invoke_options={        "body": {"name": "Functions"},    },)
```

* * *

## Subscribe to channel

- By default, Broadcast and Presence are enabled for all projects.
- By default, listening to database changes is disabled for new projects due to database performance and security concerns. You can turn it on by managing Realtime's [replication](https://supabase.com/docs/guides/api#realtime-api-overview).
- You can receive the "previous" data for updates and deletes by setting the table's `REPLICA IDENTITY` to `FULL` (e.g., `ALTER TABLE your_table REPLICA IDENTITY FULL;`).
- Row level security is not applied to delete statements. When RLS is enabled and replica identity is set to full, only the primary key is sent to clients.

Listen to broadcast messagesListen to presence syncListen to presence joinListen to presence leaveListen to all database changesListen to a specific tableListen to insertsListen to updatesListen to deletesListen to multiple eventsListen to row level changes

```flex

1
2
3
4
5
6
7
8
9
10
11
12
13
channel = supabase.channel("room1")def on_subscribe(status, err):    if status == RealtimeSubscribeStates.SUBSCRIBED:        channel.send_broadcast(            "cursor-pos",             {"x": random.random(), "y": random.random()}        )def handle_broadcast(payload):    print("Cursor position received!", payload)channel.on_broadcast(event="cursor-pos", callback=handle_broadcast).subscribe(on_subscribe)
```

* * *

## Unsubscribe from a channel

- Removing a channel is a great way to maintain the performance of your project's Realtime service as well as your database if you're listening to Postgres changes. Supabase will automatically handle cleanup 30 seconds after a client is disconnected, but unused channels may cause degradation as more clients are simultaneously subscribed.

Removes a channel

```flex

1
supabase.remove_channel(myChannel)
```

* * *

## Unsubscribe from all channels

- Removing channels is a great way to maintain the performance of your project's Realtime service as well as your database if you're listening to Postgres changes. Supabase will automatically handle cleanup 30 seconds after a client is disconnected, but unused channels may cause degradation as more clients are simultaneously subscribed.

Remove all channels

```flex

1
supabase.remove_all_channels()
```

* * *

## Retrieve all channels

Get all channels

```flex

1
channels = supabase.get_channels()
```

* * *

## Broadcast a message

Broadcast a message to all connected clients to a channel.

Send a message via websocket

```flex

1
2
3
4
5
6
7
channel = supabase.channel("room1")def on_subscribe(status, err):    if status == RealtimeSubscribeStates.SUBSCRIBED:        channel.send_broadcast('cursor-pos', {"x": random.random(), "y": random.random()})channel.subscribe(on_subscribe)
```

Response

* * *

## Create a bucket

Creates a new Storage bucket

- RLS policy permissions required:
  - `buckets` table permissions: `insert`
  - `objects` table permissions: none
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- idRequiredstring



A unique identifier for the bucket you are creating.

- optionsRequiredCreateOrUpdateBucketOptions

Details


Create bucket

```flex

1
2
3
4
5
6
7
8
9
10
11
response = (    supabase.storage    .create_bucket(        "avatars",        options={            "public": False,            "allowed_mime_types": ["image/png"],            "file_size_limit": 1024,        }    ))
```

Response

* * *

## Retrieve a bucket

Retrieves the details of an existing Storage bucket.

- RLS policy permissions required:
  - `buckets` table permissions: `select`
  - `objects` table permissions: none
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- idRequiredstring



The unique identifier of the bucket you would like to retrieve.


Get bucket

```flex

1
response = supabase.storage.get_bucket("avatars")
```

Response

* * *

## List all buckets

Retrieves the details of all Storage buckets within an existing project.

- RLS policy permissions required:
  - `buckets` table permissions: `select`
  - `objects` table permissions: none
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

List buckets

```flex

1
response = supabase.storage.list_buckets()
```

Response

* * *

## Update a bucket

Updates a Storage bucket

- RLS policy permissions required:
  - `buckets` table permissions: `select` and `update`
  - `objects` table permissions: none
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- idRequiredstring



A unique identifier for the bucket you are creating.

- optionsRequiredCreateOrUpdateBucketOptions

Details


Update bucket

```flex

1
2
3
4
5
6
7
8
9
10
11
response = (    supabase.storage    .update_bucket(        "avatars",        options={            "public": False,            "allowed_mime_types": ["image/png"],            "file_size_limit": 1024,        }    ))
```

Response

* * *

## Delete a bucket

Deletes an existing bucket. A bucket can't be deleted with existing objects inside it. You must first `empty()` the bucket.

- RLS policy permissions required:
  - `buckets` table permissions: `select` and `delete`
  - `objects` table permissions: none
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- idRequiredstring



The unique identifier of the bucket you would like to delete.


Delete bucket

```flex

1
response = supabase.storage.delete_bucket("avatars")
```

Response

* * *

## Empty a bucket

Removes all objects inside a single bucket.

- RLS policy permissions required:
  - `buckets` table permissions: `select`
  - `objects` table permissions: `select` and `delete`
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- idRequiredstring



The unique identifier of the bucket you would like to empty.


Empty bucket

```flex

1
response = supabase.storage.empty_bucket("avatars")
```

Response

* * *

## Upload a file

Uploads a file to an existing bucket.

- RLS policy permissions required:
  - `buckets` table permissions: none
  - `objects` table permissions: only `insert` when you are uploading new files and `select`, `insert` and `update` when you are upserting files
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works
- Please specify the appropriate content [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) if you are uploading images or audio. If no `file_options` are specified, the MIME type defaults to `text/html`.

### Parameters

- pathRequiredstring



The file path, including the file name. Should be of the format `folder/subfolder/filename.png`. The bucket must already exist before attempting to upload.

- fileRequiredBufferedReader \| bytes \| FileIO \| string \| Path



The body of the file to be stored in the bucket.

- file\_optionsRequiredFileOptions

Details


Upload file using filepath

```flex

1
2
3
4
5
6
7
8
9
10
with open("./public/avatar1.png", "rb") as f:    response = (        supabase.storage        .from_("avatars")        .upload(            file=f,            path="public/avatar1.png",            file_options={"cache-control": "3600", "upsert": "false"}        )    )
```

Response

* * *

## Download a file

Downloads a file from a private bucket. For public buckets, make a request to the URL returned from `get_public_url` instead.

- RLS policy permissions required:
  - `buckets` table permissions: none
  - `objects` table permissions: `select`
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- pathRequiredstring



The full path and file name of the file to be downloaded. For example `folder/image.png`.

- optionsRequiredDownloadOptions

Details


Download fileDownload file with transformations

```flex

1
2
3
4
5
6
7
with open("./myfolder/avatar1.png", "wb+") as f:    response = (        supabase.storage        .from_("avatars")        .download("folder/avatar1.png")    )    f.write(response)
```

* * *

## List all files in a bucket

Lists all the files within a bucket.

- RLS policy permissions required:
  - `buckets` table permissions: none
  - `objects` table permissions: `select`
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- pathOptionalstring



The folder path.

- optionsOptionalSearchOptions

Details


List files in a bucketSearch files in a bucket

```flex

1
2
3
4
5
6
7
8
9
10
11
12
response = (    supabase.storage    .from_("avatars")    .list(        "folder",        {            "limit": 100,            "offset": 0,            "sortBy": {"column": "name", "order": "desc"},        }    ))
```

Response

* * *

## Replace an existing file

Replaces an existing file at the specified path with a new one.

- RLS policy permissions required:
  - `buckets` table permissions: none
  - `objects` table permissions: `update` and `select`
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- pathRequiredstring



The file path, including the file name. Should be of the format `folder/subfolder/filename.png`. The bucket must already exist before attempting to upload.

- fileRequiredBufferedReader \| bytes \| FileIO \| string \| Path



The body of the file to be stored in the bucket.

- file\_optionsRequiredFileOptions

Details


Update file

```flex

1
2
3
4
5
6
7
8
9
10
with open("./public/avatar1.png", "rb") as f:    response = (        supabase.storage        .from_("avatars")        .update(            file=f,            path="public/avatar1.png",            file_options={"cache-control": "3600", "upsert": "true"}        )    )
```

Response

* * *

## Move an existing file

Moves an existing file to a new path in the same bucket.

- RLS policy permissions required:
  - `buckets` table permissions: none
  - `objects` table permissions: `update` and `select`
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- from\_pathRequiredstring



The original file path, including the current file name. For example `folder/image.png`.

- to\_pathRequiredstring



The new file path, including the new file name. For example `folder/image-new.png`.


Move file

```flex

1
2
3
4
5
6
7
8
response = (    supabase.storage    .from_("avatars")    .move(        "public/avatar1.png",         "private/avatar2.png"    ))
```

Response

* * *

## Copy an existing file

Copies an existing file to a new path in the same bucket.

- RLS policy permissions required:
  - `buckets` table permissions: none
  - `objects` table permissions: `update` and `select`
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- from\_pathRequiredstring



The original file path, including the current file name. For example `folder/image.png`.

- to\_pathRequiredstring



The new file path, including the new file name. For example `folder/image-new.png`.


Copy file

```flex

1
2
3
4
5
6
7
8
response = (    supabase.storage    .from_("avatars")    .copy(        "public/avatar1.png",         "private/avatar2.png"    ))
```

Response

* * *

## Delete files in a bucket

Deletes files within the same bucket

- RLS policy permissions required:
  - `buckets` table permissions: none
  - `objects` table permissions: `delete` and `select`
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- pathsRequiredlist\[string\]



An array of files to delete, including the path and file name. For example `["folder/image.png"]`.


Delete file

```flex

1
2
3
4
5
response = (    supabase.storage    .from_("avatars")    .remove(["folder/avatar1.png"]))
```

Response

* * *

## Create a signed URL

Creates a signed URL for a file. Use a signed URL to share a file for a fixed amount of time.

- RLS policy permissions required:
  - `buckets` table permissions: none
  - `objects` table permissions: `select`
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- pathRequiredstring



The file path, including the file name. For example `"folder/image.png"`.

- expires\_inRequirednumber



The number of seconds until the signed URL expires. For example, `60` for URLs which are valid for one minute.

- optionsOptionalURLOptions

Details


Create Signed URLCreate a signed URL for an asset with transformationsCreate a signed URL which triggers the download of the asset

```flex

1
2
3
4
5
6
7
8
response = (    supabase.storage    .from_("avatars")    .create_signed_url(        "folder/avatar1.png",         60    ))
```

Response

* * *

## Create signed URLs

Creates multiple signed URLs. Use a signed URL to share a file for a fixed amount of time.

- RLS policy permissions required:
  - `buckets` table permissions: none
  - `objects` table permissions: `select`
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- pathsRequiredlist\[string\]



The file paths to be downloaded, including the current file names. For example `["folder/image.png", "folder2/image2.png"]`.

- expires\_inRequirednumber



The number of seconds until the signed URLs expire. For example, `60` for URLs which are valid for one minute.

- optionsOptionalCreateSignedURLsOptions

Details


Create Signed URLs

```flex

1
2
3
4
5
6
7
8
response = (    supabase.storage    .from_("avatars")    .create_signed_urls(        ["folder/avatar1.png", "folder/avatar2.png"],         60    ))
```

Response

* * *

## Create signed upload URL

Creates a signed upload URL. Signed upload URLs can be used to upload files to the bucket without further authentication. They are valid for 2 hours.

- RLS policy permissions required:
  - `buckets` table permissions: none
  - `objects` table permissions: `insert`
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- pathRequiredstring



The file path, including the current file name. For example `"folder/image.png"`.


Create Signed URL

```flex

1
2
3
4
5
response = (    supabase.storage    .from_("avatars")    .create_signed_upload_url("folder/avatar1.png"))
```

Response

* * *

## Upload to a signed URL

Upload a file with a token generated from `create_signed_upload_url`.

- RLS policy permissions required:
  - `buckets` table permissions: none
  - `objects` table permissions: none
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- pathRequiredstring



The file path, including the file name. Should be of the format `folder/subfolder/filename.png`. The bucket must already exist before attempting to upload.

- tokenRequiredstring



The token generated from `create_signed_upload_url`

- fileRequiredBufferedReader \| bytes \| FileIO \| string \| Path



The body of the file to be stored in the bucket.

- optionsRequiredFileOptions

Details


Create Signed URL

```flex

1
2
3
4
5
6
7
8
9
10
with open("./public/avatar1.png", "rb") as f:    response = (        supabase.storage        .from_("avatars")        .upload_to_signed_url(            path="folder/cat.jpg",            token="token-from-create_signed_upload_url",            file=f,        )    )
```

Response

* * *

## Retrieve public URL

A simple convenience function to get the URL for an asset in a public bucket. If you do not want to use this function, you can construct the public URL by concatenating the bucket URL with the path to the asset. This function does not verify if the bucket is public. If a public URL is created for a bucket which is not public, you will not be able to download the asset.

- The bucket needs to be set to public, either via [update\_bucket()](https://supabase.com/docs/reference/python/storage-updatebucket) or by going to Storage on [supabase.com/dashboard](https://supabase.com/dashboard), clicking the overflow menu on a bucket and choosing "Make public"
- RLS policy permissions required:
  - `buckets` table permissions: none
  - `objects` table permissions: none
- Refer to the [Storage guide](https://supabase.com/docs/guides/storage/security/access-control) on how access control works

### Parameters

- pathRequiredstring



The path and name of the file to generate the public URL for. For example `folder/image.png`.

- optionsOptionalURLOptions

Details


Returns the URL for an asset in a public bucketReturns the URL for an asset in a public bucket with transformationsReturns the URL which triggers the download of an asset in a public bucket

```flex

1
2
3
4
5
response = (    supabase.storage    .from_("avatars")    .get_public_url("folder/avatar1.jpg"))
```

Response

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings