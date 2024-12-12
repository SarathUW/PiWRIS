## Project layout
    .github/workflows/
        python-package-conda.yml # lists dependencies
    docs/
        logos/
            PyWRIS_logo.png # PyWRIS logo
        components.md # List of possible use cases and components
        technology_review_by_library.md # comparisons of 3 possible libraries we considered using, listed by package.
        technology_review_by_library.md # comparisons of 3 possible libraries we considered using, listed by metrics.
        user_stories.md # some hypothetical users and their reasons for using PyWRIS
    mkdocs/ # documentation using mkdocs
        docs/
            assets/
              PyWRIS_logo.png # PyWRIS logo (added for ease of relative path) 
            commands.md # list of functions and what they do
            dir.md # project directory layout
            explanation.md # {wip}
            howto.md # {wip}
            index.md # homepage
            tutorials.md # example usage of functions
        mkdocs.yml # site configuration
    src/pywris/
        geo_units/
            components.py # defines some classes
        static_data/
            request_urls.py # list urls, payloads, and methods of WRIS requests
            state_ids.py # dictionary of all state names and their codes
        surface_water/
            storage/
                reservoir.py # defines functions used in reservoir data fetching
        utils/
            fetch_wris.py # get information from the India WRIS website
        visualization/
            plot.py # plotting functions
        pywris.py # hydroframe information
    tests/
        geo_units/
            test_components.py # testing, mocks, and patches of classes
        surface_water/
            storage/
                test_reservoir.py # testing, mocks, and patches for reservoir functions
        visualization/
            test_plots.py # testing, mocks, and patches for plotting
        test_pywris.py # unit tests, mocks and patches
    LICENSE # licensing information
    README.md # README file with information to get started
    pyproject.toml # set up pywris package
