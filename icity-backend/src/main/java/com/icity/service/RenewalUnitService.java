package com.icity.service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.icity.entity.RenewalUnit;
import com.icity.mapper.RenewalUnitMapper;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class RenewalUnitService extends ServiceImpl<RenewalUnitMapper, RenewalUnit> {

    public List<RenewalUnit> getAllUnitsWithGeo() {
        return baseMapper.getAllUnits();
    }

    public RenewalUnit getUnitDetail(Integer id) {
        return baseMapper.getUnitById(id);
    }
}