package com.icity.service;

import com.icity.entity.Poi;
import com.icity.mapper.PoiMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class PoiService {

    @Autowired
    private PoiMapper poiMapper;

    public List<Poi> getPoisByUnitAndYear(Long unitId, Integer year) {
        return poiMapper.findByUnitIdAndYear(unitId, year);
    }
}
