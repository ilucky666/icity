package com.icity.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("wuhan_renewal_pois_unified")
public class Poi {
    private Long unitId;
    private String unitName;
    private String poiName;
    private String originalType;
    private String unifiedCategory;
    private Integer obsYear;
    private String geom; // PostGIS geometry serialized as string (e.g. GeoJSON or WKT)
}
