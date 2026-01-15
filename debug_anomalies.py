from backend.dashboard_service import dashboard_service
from backend.model_service import model_service

model_service.load_resources()
report = dashboard_service.get_full_risk_report()

print(f"Total entries in risk report: {len(report)}")
print("Sample entries:")
for r in report[:5]:
    print(f" - {r.state} / {r.district}: {r.status} (Vol: {r.prediction})")

# Test filtering capability (simulated)
mh_districts = [r for r in report if r.state == 'Maharashtra']
print(f"Maharashtra districts count: {len(mh_districts)}")
