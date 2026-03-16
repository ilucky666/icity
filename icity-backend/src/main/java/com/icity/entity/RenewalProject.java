package com.icity.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.io.Serializable;

@Data
@TableName("sys_renewal_project")
public class RenewalProject implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(value = "id", type = IdType.AUTO)
    private Integer id;

    private String name;

    private Integer renewalYear;

    private Double area;

    // We will use a custom query or a TypeHandler to handle geometry. 
    // For simplicity in this demo, we might fetch it as GeoJSON string in a DTO or separate field.
    // Here we just map the column, but we might need to use a spatial library or just ignore it in default select 
    // and fetch it specifically when needed as GeoJSON.
    // Let's assume we use a string for GeoJSON representation for the frontend.
    @TableField(exist = false)
    private String geojson; 
}
