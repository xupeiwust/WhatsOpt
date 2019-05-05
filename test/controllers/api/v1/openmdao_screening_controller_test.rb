require 'test_helper'
require 'json'

class Api::V1::OpenmdaoScreeningControllerTest < ActionDispatch::IntegrationTest
  setup do
    user1 = users(:user1)
    @auth_headers = {"Authorization" => "Token " + TEST_API_KEY}
    @ope = operations(:screening)
  end
  
  test "should run openmdao screening" do
    get api_v1_operation_openmdao_screenings_new_url(@ope), as: :json, headers: @auth_headers
    assert_response :success
    sa = JSON.parse(response.body)
    expected = { "mu" => [0.65, 0.21000000000000005], 
                 "mu_star" => [1.62, 0.3500000000000001], 
                 "sigma" => [1.794107020219251, 0.41199514560246936], 
                 "names" => ["x1", "z"]}
    assert_equal expected, sa['sensitivity'] 
  end
  
end
