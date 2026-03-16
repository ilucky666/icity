package com.icity.controller;

import com.icity.entity.RenewalUnit;
import com.icity.service.RenewalUnitService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/unit")
@CrossOrigin(origins = "*") // Allow frontend access
public class RenewalUnitController {

    @Autowired
    private RenewalUnitService renewalUnitService;

    @GetMapping("/list")
    public List<RenewalUnit> listUnits() {
        return renewalUnitService.getAllUnitsWithGeo();
    }

    @GetMapping("/detail/{id}")
    public RenewalUnit getUnitDetail(@PathVariable Integer id) {
        return renewalUnitService.getUnitDetail(id);
    }
}