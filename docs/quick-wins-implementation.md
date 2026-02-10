# Quick Wins: Immediate Dashboard Enhancements

## Top 3 Highest-Value, Lowest-Effort Additions

### 1. Site Performance Comparison (2-3 hours)

**What:** Bar chart showing satisfaction score by site location

**Why:** DPD has multiple sites (Toulouse, Lyon, Paris, etc.). Site Managers need to see how their location compares.

**Implementation:**
```javascript
// New component: SitePerformanceChart.vue
// Data aggregation:
const siteStats = conversations.reduce((acc, conv) => {
  const site = conv.metadata.site;
  if (!acc[site]) {
    acc[site] = { total: 0, positive: 0, neutral: 0, negative: 0 };
  }
  acc[site].total++;
  acc[site][conv.sentiment]++;
  return acc;
}, {});

// Calculate satisfaction % per site
const siteSatisfaction = Object.entries(siteStats).map(([site, stats]) => ({
  site,
  satisfaction: (stats.positive / stats.total) * 100,
  volume: stats.total
}));
```

**Visual:**
- Horizontal bar chart
- Green bars for above-average sites
- Red bars for below-average sites
- Click bar → filter dashboard to that site

---

### 2. Channel Sentiment Comparison (1-2 hours)

**What:** Side-by-side comparison of Email vs Call sentiment

**Why:** Identifies if one channel needs improvement. Sample data shows both email and call types.

**Implementation:**
```javascript
// Add to KPICards or new component
const channelStats = conversations.reduce((acc, conv) => {
  const channel = conv.type; // 'email' or 'call'
  if (!acc[channel]) {
    acc[channel] = { total: 0, positive: 0, neutral: 0, negative: 0 };
  }
  acc[channel].total++;
  acc[channel][conv.sentiment]++;
  return acc;
}, {});

// Calculate sentiment % per channel
const channelSentiment = {
  email: {
    positive: (channelStats.email?.positive / channelStats.email?.total) * 100,
    negative: (channelStats.email?.negative / channelStats.email?.total) * 100
  },
  call: {
    positive: (channelStats.call?.positive / channelStats.call?.total) * 100,
    negative: (channelStats.call?.negative / channelStats.call?.total) * 100
  }
};
```

**Visual:**
- Two donut charts side-by-side (Email | Call)
- Or stacked bar chart
- Insight text: "Email complaints are X% higher than calls"

---

### 3. Functional Filters (2-3 hours)

**What:** Make the header filter dropdowns actually filter the dashboard

**Why:** Currently filters are static. Making them functional enables segmentation analysis.

**Implementation:**
```javascript
// In Dashboard.vue, add reactive filters
data() {
  return {
    filters: {
      organization: 'DPD',
      team: 'Toutes les équipes',
      project: 'Tous les projets',
      dateRange: null
    }
  };
},
computed: {
  filteredData() {
    // Filter conversations based on active filters
    // Pass to child components via props
  }
}
```

**Visual:**
- Dropdowns in header become functional
- Add date range picker
- "Clear filters" button
- Show active filter count badge

---

## Sample Data Insights (From Current Dataset)

### Key Findings from conversations.json:

1. **Top Negative Themes:**
   - "Performance Livraison" (delivery delays) - 37% negative
   - "Qualité & État" (package condition) - 44% negative
   - "Gestion des réclamations" (claim handling) - 72% negative

2. **Site Distribution:**
   - Toulouse: 3 conversations (2 negative, 1 positive)
   - Lyon: 3 conversations (1 negative, 2 positive)
   - Paris: 3 conversations (1 negative, 2 positive)
   - Multiple other sites represented

3. **Channel Pattern:**
   - Email: 15 conversations
   - Call: 15 conversations
   - Need to analyze sentiment difference

4. **Recurring Issues:**
   - "Délai non respecté" (delay not respected) - appears in multiple verbatims
   - "Réclamation non traitée" (unprocessed claim) - appears multiple times
   - "Colis endommagé" (damaged package) - recurring theme

---

## DPD-Specific Quick Insights

### From Customer Domain Description:

DPD focuses on:
- **Last-mile delivery** → Track "Performance Livraison" sentiment by site
- **Pickup points (DPD Pickup)** → Analyze "Options & Flexibilité" sentiment
- **Digital tools (DPD Predict)** → Track "Digitalisation" sentiment
- **Sustainability** → Could add theme for eco-friendly feedback

### Actionable Recommendations:

1. **Delivery Window Accuracy:**
   - If DPD Predict provides time slots, track sentiment for on-time vs late deliveries
   - Sample data mentions "créneaux horaires" (time slots)

2. **Pickup Point Satisfaction:**
   - Sample data mentions "points relais" (pickup points)
   - Track sentiment for home delivery vs pickup point delivery

3. **Driver Professionalism:**
   - Sample data includes positive feedback about "chauffeur professionnel"
   - Could extract driver-related sentiment as separate metric

---

## Implementation Checklist

### Phase 1: Quick Wins (This Sprint)
- [ ] Site Performance Comparison chart
- [ ] Channel Sentiment Analysis widget
- [ ] Functional filters (organization, team, date range)
- [ ] Add "Clear filters" button

### Phase 2: Enhanced Insights (Next Sprint)
- [ ] Top Negative Themes Trend (sparklines)
- [ ] Geographic Heatmap (if site coordinates available)
- [ ] Export to Excel functionality
- [ ] Comparative period analysis (this month vs last)

### Phase 3: Advanced Features (Future)
- [ ] Action Items Generator
- [ ] Root Cause Chain Analysis
- [ ] Predictive Deterioration Alerts
- [ ] PDF Report Generation

---

## Code Structure Recommendations

### New Components to Create:

```
src/components/
├── SitePerformanceChart.vue      # Site comparison
├── ChannelComparison.vue          # Email vs Call
├── TrendSparkline.vue            # Mini trend charts
├── FilterBar.vue                 # Enhanced filter component
└── ExportButton.vue              # Export functionality
```

### Data Service Enhancements:

```javascript
// src/services/dataService.js
export const dataService = {
  // Existing methods...
  
  // New methods:
  getSitePerformance() {
    // Aggregate by site
  },
  getChannelComparison() {
    // Aggregate by type (email/call)
  },
  getFilteredData(filters) {
    // Apply filters to all data
  },
  exportToExcel(filters) {
    // Generate Excel export
  }
};
```

---

## Success Criteria

After implementing quick wins:
- ✅ Site Managers can see their site's performance vs others
- ✅ CX Director can identify if email handling needs improvement
- ✅ Users can filter dashboard by site/team/date
- ✅ Export functionality enables stakeholder reporting

**Expected Impact:**
- 30% increase in dashboard usage (from actionable insights)
- Faster decision-making (site-level visibility)
- Better resource allocation (identify problem areas)

