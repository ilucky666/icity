package com.icity.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.icity.entity.RenewalProject;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Param;
import java.util.List;
import java.util.Map;

@Mapper
public interface RenewalProjectMapper extends BaseMapper<RenewalProject> {

    @Select("SELECT id, name, renewal_year, area, ST_AsGeoJSON(geom) as geojson FROM sys_renewal_project")
    List<RenewalProject> getAllProjects();

    @Select("SELECT id, name, renewal_year, area, ST_AsGeoJSON(geom) as geojson FROM sys_renewal_project WHERE id = #{id}")
    RenewalProject getProjectById(@Param("id") Integer id);
    
    // For the detail statistics
    @Select("SELECT type, COUNT(*) as count FROM sys_amenity WHERE ST_DWithin(geom, (SELECT geom FROM sys_renewal_project WHERE id = #{projectId}), 500, true) GROUP BY type")
    List<Map<String, Object>> getAmenityStats(@Param("projectId") Integer projectId);
    
    // For enterprise stats (mock query as we don't have year column in enterprise usually, but assuming logic based on requirements)
    @Select("SELECT COUNT(*) FROM sys_enterprise WHERE ST_Contains((SELECT geom FROM sys_renewal_project WHERE id = #{projectId}), geom)")
    Integer getEnterpriseCount(@Param("projectId") Integer projectId);
}
