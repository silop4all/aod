# Change Log

## 2017-04-18
- Finalize the community-based support
- Implement the service rating (include multiple metrics, adv/dis)
- Implement the QoS-cost aware filtering
- Implement the Try different approach
- Search services via keywords  
    + render the same presentation template for any type of search


## 2017-02-28
- Updates:
    + remove placeholder from login form
    + resize & limit the title of services    
    + hide not working preferences from top menu
    + filter the length of articles, change header size (customized index)
    + hide geographical constraints from service preview (if not exists)
    + increase the maximun chars threshold in service description (4K)
    + fix conflict among app logo and user logo
    + fix links and images included in articles (customized index)

## 2017-02-10
- Add modules for paypal, payment component
- Add Paypal btn in service preview (customer perspective)


## 2017-02-02
- Publish task in ML (required integration with IAM)

## 2016-12-08
- Browse services without login


## 2016-11-28
- Update REST API
- Fixes:
    + filter services per provider in provider dashboard
    + diplay provider full name in service display


## 2016-11-21
- Capability to associate a service with one or more FAQ articles (admin panel)
- Implement the customized search engine
    + load services/products and relative FAQ articles that meet the user input (filters)
    + search is achieved by invoking REST web services
- Declare the customization state in project settings
- Detect broken technical support links on demand performing HTTP HEAD request
- Multiple links for technical support of service
    + shared links (new tab in browser)
    + embed youTube/vimeo videos
    + documents (office, pdf)
    + audio/video (mp3/mp4)
- Refactor provider dashboard
- Refactor some urls/templates absolute paths 
- Fix bugs:
    + upload image in service registration (POST method)


## 2016-10-31
- Implementations:
    + Multilingual features
        * translate JS variables in admin-rosetta interface for supported languages
        * translate HTML variables in admin-rosetta interface for supported languages
        * support mechanism to translate specific text/string fields in database models for supported languages
        * implement mechanism to alter languages in app UI
        * manage icons for the the available languagesin admin panel (image versioning is supported)
        * implement middleware to sync cookie language code with session language code
    + AoD technical support
        * admin add new topics or manage topics
        * admin associate N articles in each topic and manage them
        * admin associate N documents in each article and manage them
        * admin associate N videos/audio files in each article and manage them
        * integrate CKeditor in AoD admin panel for articles population
        * add topics in AoD footer
        * admin sets topics/articles as visible or not
        * admin limits the public access or not in a set of topics/articles
        * admin provides translation in available languages
    + Presentation themes mechanism 
        * admin manages the themes of the application
        * admin generates themes based on LESS code
        * end-user denotes a theme as favorite
        * Aod stores cookie for user theme
    + Manage app's logo and title from admin panel
    + Manage the links of the related with app social networks from admin panel
    + Load components status using the app_processor
    + Load metadata (size, paths, dimension etc) for images/docs/videos in admin 
    + Manage cookie policy from admininstraton panel (supported in all available languages)
    + Generate sitemap for app (os for a subset of urls)
    + Generate robots.txt for SEO and manage it from admin panel
    + Enable page preloader if UI options is disabled
- Improvements:
    + refactor preferences navbar menu
    + detect broken links
    + update service attributes and simplify the service registration/modification process
    + enrich the AoD API
    + refactor settings files
- Integrations with AoD:
    + integrate Social Network based on IAM
        * sync users, sessions, login & logout processes
    + integrate UI options (Cloud4all EU project)
    + integrate crowd funding application 
- Fix bugs:
    + replace the service title used in a subset of endpoints with pk
    + ensure that models (carers,consumers, provoiders, user, services etc) works smoothly in admin panel
    + update some db models 
    + fix logout mechanism
    + fix bootstrap table localization
    + prevent from multiple depiction of the same service as search result both in AoD app and AoD admin panel
    + unlocalize values, numbers, coordinates in GUI forms
    + improve mobile view
    + minor updates/fixes in javascript files
    

## 2016-09-09
- AoD implementation enchancements:
    + redesign the top menu
    + integrate Google analytics 
    + list in Google search engine
    + add the list of supported languages in top menu 
    + prepare multilingual feature in templates (WIP)
    + set cors in settings
    + set developement & deployment settings
    + set swagger settings to work on deployment environment
    + serve the media files via apache server in production mode
    + integration with IAM
    + update requirements
- AoD admin implementation enchancements:
    +  integrate with rosseta plugin
    +  integrate with dowser plugin
- Fixes:
    + use urls namespace & name per application

