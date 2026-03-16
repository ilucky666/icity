package com.icity;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.icity.mapper")
public class IcityApplication {

    public static void main(String[] args) {
        SpringApplication.run(IcityApplication.class, args);
    }

}
