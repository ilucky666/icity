package com.icity.service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.icity.entity.RenewalProject;
import com.icity.mapper.RenewalProjectMapper;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

@Service
public class RenewalProjectService extends ServiceImpl<RenewalProjectMapper, RenewalProject> {

    public List<RenewalProject> getAllProjectsWithGeo() {
        return baseMapper.getAllProjects();
    }

    public Map<String, Object> getProjectDetail(Integer id) {
        RenewalProject project = baseMapper.getProjectById(id);
        if (project == null) return null;
        
        List<Map<String, Object>> amenities = baseMapper.getAmenityStats(id);
        Integer enterpriseCount = baseMapper.getEnterpriseCount(id);
        
        // Mocking patent data growth for chart based on project ID to have some variation
        Map<String, Integer> patentGrowth = new HashMap<>();
        int base = (id % 5 + 1) * 5; 
        patentGrowth.put("2020", base);
        patentGrowth.put("2021", base + (int)(Math.random() * 5));
        patentGrowth.put("2022", base + 5 + (int)(Math.random() * 10));
        patentGrowth.put("2023", base + 15 + (int)(Math.random() * 20));

        Map<String, Object> result = new HashMap<>();
        result.put("project", project);
        result.put("amenities", amenities);
        result.put("enterpriseCount", enterpriseCount);
        result.put("patentGrowth", patentGrowth);
        
        return result;
    }
}
