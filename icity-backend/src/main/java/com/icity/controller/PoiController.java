package com.icity.controller;

import com.icity.entity.Poi;
import com.icity.service.PoiService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/poi")
@CrossOrigin(origins = "*")
public class PoiController {

    @Autowired
    private PoiService poiService;

    @GetMapping("/list")
    public List<Poi> getPois(@RequestParam Long unitId, @RequestParam Integer year) {
        return poiService.getPoisByUnitAndYear(unitId, year);
    }
}
