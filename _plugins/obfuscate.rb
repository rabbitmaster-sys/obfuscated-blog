# _plugins/obfuscate.rb
module Jekyll
  module ObfuscateFilter
    def obfuscate(input)
      map = {
        'A' => "\uE001", 'B' => "\uE002", 'C' => "\uE003",
        'D' => "\uE004", 'E' => "\uE005", 'F' => "\uE006",
        'G' => "\uE007", 'H' => "\uE008", 'I' => "\uE009",
        'J' => "\uE00A", 'K' => "\uE00B", 'L' => "\uE00C",
        'M' => "\uE00D", 'N' => "\uE00E", 'O' => "\uE00F",
        'P' => "\uE010", 'Q' => "\uE011", 'R' => "\uE012",
        'S' => "\uE013", 'T' => "\uE014", 'U' => "\uE015",
        'V' => "\uE016", 'W' => "\uE017", 'X' => "\uE018",
        'Y' => "\uE019", 'Z' => "\uE01A"
      }

      input.chars.map { |c| map[c] || c }.join
    end
  end
end

Liquid::Template.register_filter(Jekyll::ObfuscateFilter)
