## Project layout
    .github/workflows/
        python-package-conda.yml # lists dependencies
    docs/
        logos/
            PyWRIS_logo.png # PyWRIS main image
        components.md # List of possible use cases and components
        technology_review_by_library.md # comparisons of 3 possible libraries we considered using, listed by package.
        technology_review_by_library.md # comparisons of 3 possible libraries we considered using, listed by metrics.
        user_stories.md # some hypothetical users and their reasons for using PyWRIS
    src/pywris/
        country_data/
            state_codes.py # dictionary of all state names and their codes
        surface_water/
            storage/
                reservoir.py # defines functions used in reservoir data fetching
        utils/
            fetch_wris.py # get information from the India WRIS website
        pywris.py # {wip}
        pywris_main.py # {wip}
    test/
        test_pywris.py # file for testing with pytest
    LICENSE # licensing information
    README.md # README file with information to get started
    pyproject.toml # set up pywris package
    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
