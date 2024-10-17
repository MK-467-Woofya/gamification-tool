# run_tests.ps1
# before start: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# by default: .\run_tests.ps1
# or you may wanna run specific test? .\run_tests.ps1 -TestPath "leaderboard.tests.test_edge_cases"
# or specific class? .\run_tests.ps1 -TestPath "leaderboard.tests.test_edge_cases.LeaderboardEdgeCasesTests"
# or specific function? .\run_tests.ps1 -TestPath "leaderboard.tests.test_edge_cases.LeaderboardEdgeCasesTests.test_leaderboard_with_boundary_dates"


param(
    [string]$TestPath = "leaderboard.tests"  # run leaderboard.tests by default
)

# show help
if ($TestPath -eq "-h" -or $TestPath -eq "--help") {
    Write-Host "Usage: .\run_tests.ps1 [-TestPath <TestPath>]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -TestPath    Specify the test path to run (default: leaderboard.tests)"
    Write-Host "               Examples:"
    Write-Host "                 leaderboard.tests"
    Write-Host "                 leaderboard.tests.test_edge_cases"
    Write-Host "                 leaderboard.tests.test_edge_cases.LeaderboardEdgeCasesTests"
    Write-Host "                 leaderboard.tests.test_edge_cases.LeaderboardEdgeCasesTests.test_method"
    exit
}

# clear docker env
docker-compose down --volumes --remove-orphans

# stop 5 second to wait all containers stop
Start-Sleep -Seconds 5

# run test
docker-compose run api python manage.py test $TestPath --noinput -v 2
