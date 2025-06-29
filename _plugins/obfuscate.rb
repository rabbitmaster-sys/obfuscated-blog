require 'nokogiri'
require 'json'

file = File.read('_plugins/map.json')
MAP = JSON.parse(file)

module Jekyll
  module Obfuscate
    SKIP_TAGS = ['script', 'style', 'code', 'pre']

    def obfuscate(input)
      doc = Nokogiri::HTML::DocumentFragment.parse(input)

      doc.traverse do |node|
        if node.text? && !node.blank? && !inside_skip_tag?(node)
          node.content = node.text.chars.map do |c|
            val = MAP.fetch(c, c)
            val.is_a?(Integer) ? val.chr(Encoding::UTF_8) : val
          end.join
        end
      end

      doc.to_html
    end

    private

    def inside_skip_tag?(node)
      node.ancestors.any? { |ancestor| SKIP_TAGS.include?(ancestor.name) }
    end
  end
end

Liquid::Template.register_filter(Jekyll::Obfuscate)
