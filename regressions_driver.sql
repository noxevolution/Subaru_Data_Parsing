select * from impressions

select count(*) from impressions



select MIN(date) from impressions
where unique_id = 'Brand_Brisbane_BTQ-7_Brisbane'

CREATE TABLE IF NOT EXISTS `regressions` (
  `d_var_table_name` varchar(255) NOT NULL,
  `i_var_table_name` varchar(255) NOT NULL,
  `d_var_unique_id` varchar(255) NOT NULL, -- will be all for all variables
  `i_var_unique_id` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
   `end_date` date NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

2013-10-01
2011-08-01

insert into regressions
VALUES
('impressions','impressions', 'Brand_Brisbane_BTQ-7_Brisbane', 'ALL','2011-08-01','2013-10-01')







'Brand_Brisbane_BTQ-7_Brisbane', '2011-08-01', '0.00', 'weekly'
