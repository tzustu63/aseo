# Profile Search Filters - Design Document

## Context

Users need to efficiently filter and find profiles within the system based on role and team attributes. This feature will enhance the search experience by allowing users to narrow down results to specific criteria.

## Goals / Non-Goals

### Goals
- Enable filtering profiles by role
- Enable filtering profiles by team
- Support combined filtering (role AND team)
- Provide intuitive UI for filter selection
- Ensure filters work in real-time
- Make filters accessible and mobile-friendly

### Non-Goals
- Advanced search with text queries (different feature)
- Saved search filters (future enhancement)
- Filter analytics or recommendations (future enhancement)
- Bulk actions on filtered results (out of scope)

## Decisions

### 1. Filter Type: Multi-Select vs Single-Select

**Decision**: Use multi-select dropdowns for both role and team filters

**Rationale**:
- Users may want to see profiles from multiple roles (e.g., "Engineer" OR "Designer")
- Teams often work cross-functionally
- Provides maximum flexibility

**Alternatives considered**:
- Single-select: Too restrictive, requires multiple searches
- Radio buttons: Not scalable for many options
- Free text search: Less precise, harder to implement

### 2. Filter Logic: AND vs OR

**Decision**: 
- Within a filter (e.g., multiple roles): Use OR logic
- Between filters (role + team): Use AND logic

**Example**:
- Role: ["Engineer", "Designer"] AND Team: ["Product", "Platform"]
- Returns: Profiles that are (Engineer OR Designer) AND (in Product OR Platform team)

### 3. State Management

**Decision**: Use URL query parameters as source of truth

```typescript
// URL format
/profiles?roles=engineer,designer&teams=product,platform

// State sync
const [filters, setFilters] = useState({
  roles: parseRolesFromURL(),
  teams: parseTeamsFromURL()
});
```

**Benefits**:
- Shareable URLs
- Browser back/forward works correctly
- No complex state library needed
- Filter state persists across page refreshes

### 4. UI Component Structure

```typescript
<ProfileSearch>
  <FilterBar>
    <RoleFilter 
      selectedRoles={filters.roles}
      onChange={handleRoleChange}
    />
    <TeamFilter 
      selectedTeams={filters.teams}
      onChange={handleTeamChange}
    />
    <ClearFiltersButton onClick={clearAllFilters} />
  </FilterBar>
  <FilterTags>
    {/* Show active filters as removable tags */}
  </FilterTags>
  <SearchResults filters={filters} />
</ProfileSearch>
```

### 5. API Design

**Endpoint**: `GET /api/profiles`

**Query Parameters**:
```
?roles=engineer,designer&teams=product,platform
```

**Backend Implementation**:
```sql
SELECT * FROM profiles 
WHERE 
  role IN ('engineer', 'designer')
  AND team IN ('product', 'platform')
ORDER BY name;
```

**Performance**: Add composite index on (role, team) for faster queries

## Risks / Trade-offs

### Risk 1: Performance with Large Datasets
- **Risk**: Filtering thousands of profiles may be slow
- **Mitigation**: 
  - Add database indexes
  - Implement pagination (limit to 50 results per page)
  - Consider caching filter options (roles/teams list)

### Risk 2: Inconsistent Data
- **Risk**: Profiles may have inconsistent role or team names
- **Mitigation**:
  - Normalize role and team values on save
  - Provide dropdown with predefined options
  - Add data validation

### Risk 3: Mobile UX Challenges
- **Risk**: Multi-select dropdowns may be hard to use on mobile
- **Mitigation**:
  - Use native select on mobile when appropriate
  - Implement responsive modal for filter selection
  - Provide clear filter indicators

### Trade-offs

1. **URL-based state vs Local state**: 
   - Chose URL for shareability
   - Trade-off: Slightly more complex code

2. **Multi-select vs Single-select**:
   - Chose multi-select for flexibility
   - Trade-off: More complex UI

3. **Real-time vs Apply button**:
   - Chose real-time updates
   - Trade-off: More API calls, but better UX

## Migration Plan

### Phase 1: Basic Implementation
1. Add role filter only
2. Test with users
3. Gather feedback

### Phase 2: Team Filter
1. Add team filter
2. Implement combined filtering
3. Optimize performance

### Phase 3: Enhancements
1. Add filter persistence
2. Implement saved searches
3. Add filter suggestions

### Rollback Plan
- Feature is purely additive
- Can be disabled with feature flag
- No data migrations required

## Open Questions

1. **Should filters be mandatory or optional?**
   - Recommendation: Optional - show all results by default

2. **How many filter options are expected?**
   - Need to know for UI design (dropdown vs modal)
   - If > 20 options, consider search within filter

3. **Should we show result count for each filter option?**
   - Example: "Engineer (23)" 
   - Helps users understand data distribution
   - Recommendation: Yes, if performance allows

4. **Should filters support "NOT" logic?**
   - Example: All roles EXCEPT "Intern"
   - Recommendation: Not in v1, consider for v2

