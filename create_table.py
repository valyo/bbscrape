from get_cars import getCars


class createTable:


	def create_table(self,conn, create_table_sql):
		""" create a table from the create_table_sql statement
		:param conn: Connection object
		:param create_table_sql: a CREATE TABLE statement
		:return:
		"""
		try:
			c = conn.cursor()
			c.execute(create_table_sql)
		except Exception as e:
			print(e)


	def main(self,getCars,createTable):

		sql_create_cars_data_table = """ CREATE TABLE IF NOT EXISTS cars_data (
	annons_id VARCHAR(32),
	awd integer,
	abs integer,
	airbag integer,
	alufalg integer,
	antisladd integer,
	antispinn integer,
	auto integer,
	bluetooth integer,
	c_las integer,
	co2 varchar(16),
	color varchar(16),
	dimljus integer,
	dragkrok integer,
	eco varchar(16),
	elhissar integer,
	elspeglar integer,
	farthallare integer,
	fdator integer,
	fuel_b_hybrid integer,
	fuel_bensin integer,
	fuel_d_hybrid integer,
	fuel_diesel integer,
	gps integer,
	itrafik varchar(16),
	keyless integer,
	klima integer,
	laddhybrid integer,
	larm integer,
	ledheadl integer,
	lucka integer,
	make varchar(16),
	mileage varchar(16),
	model varchar(32),
	motor varchar(16),
	motorv integer,
	muggh integer,
	multifunktionsratt integer,
	parkassist integer,
	power varchar(16),
	pris varchar(16),
	rails integer,
	rattv integer,
	regnr integer,
	regnsensor integer,
	servo integer,
	skin integer,
	spec integer,
	startstop integer,
	stolminne integer,
	stolv_fram integer,
	svensks integer, 
	vikt varchar(16),
	vinterd_d integer,
	vinterd_fr integer,
	xenon integer,
	year varchar(16),
	ytempm integer
);"""

		# getCars = getCars()
		db = getCars.connectDB()
		
		if db is not None:
			createTable.create_table(db, sql_create_cars_data_table)
		else:
			print("Error! cannot create the database connection.")

if __name__ == '__main__':

	getCars = getCars()
	createTable = createTable()
	createTable.main(getCars,createTable)
