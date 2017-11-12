# Plugin to add environment variables to the `site` object in Liquid templates

module Jekyll

  class EnvironmentVariablesGenerator < Generator

    def generate(site)
      site.config['stripe_publishable_key'] = ENV['STRIPE_PUBLISHABLE_KEY']
    end

  end

end
