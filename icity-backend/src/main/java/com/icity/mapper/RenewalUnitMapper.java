package com.icity.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.icity.entity.RenewalUnit;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Param;
import java.util.List;

@Mapper
public interface RenewalUnitMapper extends BaseMapper<RenewalUnit> {

    @Select("SELECT id, unit_name, category, description, main_industry, investment_est, ST_AsGeoJSON(geom) as geojson FROM wuhan_renewal_units")
    List<RenewalUnit> getAllUnits();

    @Select("SELECT id, unit_name, category, description, main_industry, investment_est, ST_AsGeoJSON(geom) as geojson FROM wuhan_renewal_units WHERE id = #{id}")
    RenewalUnit getUnitById(@Param("id") Integer id);
}