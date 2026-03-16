package com.icity.controller;

import com.icity.entity.RenewalProject;
import com.icity.service.RenewalProjectService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/project")
@CrossOrigin(origins = "*") // Allow frontend access
public class RenewalProjectController {

    @Autowired
    private RenewalProjectService renewalProjectService;

    @GetMapping("/list")
    public List<RenewalProject> listProjects() {
        return renewalProjectService.getAllProjectsWithGeo();
    }

    @GetMapping("/detail/{id}")
    public Map<String, Object> getProjectDetail(@PathVariable Integer id) {
        return renewalProjectService.getProjectDetail(id);
    }
}
