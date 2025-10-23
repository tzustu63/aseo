# Add Profile Search Filters by Role and Team

## Why

Users need to efficiently find team members or profiles based on their role and team affiliation. Currently, there is no way to filter profiles, making it difficult to locate specific people in organizations with many members. Adding role and team filters will significantly improve user experience and search efficiency.

## What Changes

- **Add role filter**: Allow users to filter profiles by job role or position
- **Add team filter**: Allow users to filter profiles by team or department
- **Combined filtering**: Support filtering by both role and team simultaneously
- **Filter UI components**: Create dropdown or multi-select components for filters
- **Filter state management**: Implement filter state and URL parameter sync
- **Search results update**: Update search results in real-time based on filter selections
- **Filter persistence**: Save filter preferences in user session or local storage
- **Clear filters action**: Provide ability to reset all filters

## Impact

- **Affected specs**: New `profile-search` capability spec
- **Affected code**: 
  - Add filter components (UI)
  - Update search API endpoints or queries
  - Add filter state management
  - Update profile data model (ensure role and team fields exist)
- **User experience**: Significantly improves search efficiency and discoverability
- **Performance**: May need to optimize queries with proper indexing on role and team fields

