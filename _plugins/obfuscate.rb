require 'nokogiri'

module Jekyll
  module Obfuscate
    SKIP_TAGS = ['script', 'style', 'code', 'pre']

    def obfuscate(input)
      chars_to_map = (
        ('A'..'Z').to_a +
        ('a'..'z').to_a +
        ('0'..'9').to_a +
        [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
         ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
      )

      # Create map from chars to PUA starting at U+E001
      map = {}
      start_code = 0xE001
      chars_to_map.each_with_index do |char, idx|
        map[char] = [start_code + idx].pack("U")
      end

      doc = Nokogiri::HTML::DocumentFragment.parse(input)

      doc.traverse do |node|
        if node.text? && !node.blank? && !inside_skip_tag?(node)
          node.content = node.text.chars.map { |c| map.fetch(c, c) }.join
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
