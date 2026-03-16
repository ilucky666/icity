package com.icity.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.icity.entity.Poi;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;

@Mapper
public interface PoiMapper extends BaseMapper<Poi> {

    @Select("SELECT unit_id, unit_name, poi_name, original_type, unified_category, obs_year, " +
            "ST_AsGeoJSON(geom) as geom " +
            "FROM wuhan_renewal_pois_unified " +
            "WHERE unit_id = #{unitId} AND obs_year = #{year}")
    List<Poi> findByUnitIdAndYear(Long unitId, Integer year);
}
