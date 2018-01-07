require 'test_helper'
require 'whats_opt/cmdows_generator'

class CmdowsGeneratorTest < ActiveSupport::TestCase

  def setup
    @mda = analyses(:cicav)
    @cmdowsgen = WhatsOpt::CmdowsGenerator.new(@mda)
  end
    
  test "should generate cmdows xml" do
    content, filename = @cmdowsgen.generate
    assert_equal  Nokogiri::XML(content).xpath('//designCompetence').size, @mda.disciplines.analyses.count
    assert_equal 'cicav.cmdows', filename
  end
  
end