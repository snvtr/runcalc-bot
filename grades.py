from math   import modf
from config import DISTANCES
from get    import get_dst, get_dst_name

class Grades(object):

    __MIN_AGE = 5
    __MAX_AGE = 99

    grade_files = [
             'AgeGrade.1mi',
             'AgeGrade.5k',
             'AgeGrade.8k',
             'AgeGrade.10k',
             'AgeGrade.12k',
             'AgeGrade.15k',
             'AgeGrade.20k',
             'AgeGrade.hm',
             'AgeGrade.30k',
             'AgeGrade.42k'
             ]

    grades  = {}
    records = {}

    def __init__(self):
        '''
        inits all the dictionaries with grades
        '''
        for grade_file in self.grade_files:
            distance = get_dst(grade_file[9:])
            self.grades[distance] = {}
            self.grades[distance]['F'] = {}
            self.grades[distance]['M'] = {}
            self.records[distance] = {}
            with open('./AgeGrades/'+grade_file, 'r') as f:
                for ln in f:
                    if ln.find(':') >= 0:
                        items = ln.rstrip().split('  ')
                        gender   = items[0][0]
                        record_t = items[1]
                        self.records[distance][gender] = record_t
                        continue
                    gender = ln[0]
                    age    = int(ln[2:4].rstrip())
                    coeff  = float(ln[5:])
                    self.grades[distance][gender][age] = coeff

    def __str2time(self, time_str):
        '''
        converts string to decimal minutes
        '''
        items = time_str.rstrip().split(':')
        return float(items[0])*60 + float(items[1]) + float(items[2])/60

    def __time2str(self, time_t):
        '''
        converts decimal minutes to formatted time string
        '''
        hours = time_t // 60
        secs, mins  = modf(time_t - hours*60)
        secs = round(secs*60)
        return '{:02d}:{:02d}:{:02d}'.format(int(hours), int(mins), int(secs))

    def __get_dist_time(self, distance, gender, age):
        '''
        returns graded time in decimal minutes for distance + gender + age
        '''
        time_t = self.__str2time(self.records[distance][gender])
        graded_t = time_t/self.grades[distance][gender][age]
        return graded_t  

    def graded_result(self, distance, gender, age):
        ''' 
        gets distance+gender+age and returns formatted time string 
        '''
        return self.__time2str(self.__get_dist_time(distance, gender, age))

    def graded_percent(self, distance, gender, age, time_str):
        ''' 
        returns percentage of the Best Result for given age from distance+time+age 
        '''
        # 1) get overall record time
        record_t = self.__str2time(self.records[distance][gender])
        # 2) convert overall record time to age-graded record time
        graded_record_t = record_t/self.grades[distance][gender][age]
        # 3) get diff between result and graded record
        graded_diff = graded_record_t/self.__str2time(time_str)
        return str(round(graded_diff*100)) + '%'

    def graded_distances(self, graded_percentage, age, gender):
        ''' 
        returns a list of probable results for a set of distances from age graded percentage
        '''
        #ret_text = ''
        #for d in self.grades.keys():
        #    ret_text += '{}: placeholder\n'.format(get_dst_name(d))
        #return ret_text
        ret_text = ''
        for distance in self.records.keys():
             for d in DISTANCES.keys():
                 if distance in DISTANCES[d]:
                     pretty_distance = DISTANCES[d][0]
                     break
             record_t        = self.__str2time(self.records[distance][gender])
             graded_record_t = record_t/self.grades[distance][gender][age]
             age_graded_t    = graded_record_t/(graded_percentage/100)
             age_graded_str  = self.__time2str(age_graded_t)
             ret_text += '{}: {}\n'.format(pretty_distance, age_graded_str)
        return ret_text


def build_agegraded(dist, res, age, gender):
    g = Grades()
    return g.graded_percent(dist, gender, age, res)

def build_agedist(percent, age, gender):
    g = Grades()
    return g.graded_distances(percent, age, gender)


if __name__ == '__main__':
    g = Grades()
    print(g.graded_result('10k', 'M', 5))
    print(g.graded_result('42k', 'F', 90))
    print(g.graded_percent('10k', 'M', 50, '00:50:00'))
    print(g.graded_distances('59%', 50, 'F'))
    